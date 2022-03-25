import json, jwt, requests
from HQApi.exceptions import ApiResponseError, BannedIPError

class BaseHQApi:
    def __init__(self, token: str = None, logintoken: str = None):
        self.token = token
        self.logintoken = logintoken

    async def api(self):
        return self

    async def get_users_me(self):
        return await self.fetch("GET", "users/me")

    async def get_user(self, id: str):
        return await self.fetch("GET", "users/{}".format(id))

    async def search(self, name):
        return await self.fetch("GET", 'users?q={}'.format(name))

    async def get_payouts_me(self):
        return await self.fetch("GET", "users/me/payouts")

    async def get_show(self):
        return await self.fetch("GET", "shows/now")

    async def get_schedule(self):
        return await self.fetch("GET", 'shows/schedule')

    async def easter_egg(self, type: str = "makeItRain"):
        return await self.fetch("POST", "easter-eggs/{}".format(type))

    async def make_payout(self, email: str):
        return await self.fetch("POST", "users/me/payouts", {"email": email})

    async def send_code(self, phone: str, method: str = "sms"):
        return await self.fetch("POST", "verifications", {"phone": phone, "method": method})

    async def confirm_code(self, verificationid: str, code: int):
        return await self.fetch("POST", "verifications/{}".format(verificationid), {"code": code})

    async def register(self, verificationid: str, name: str, referral: str = None):
        return await self.fetch("POST", "users", {
            "country": "MQ==", "language": "eu",
            "referringUsername": referral,
            "username": name,
            "verificationId": verificationid})

    async def delete_avatar(self):
        return await self.fetch("DELETE", "users/me/avatarUrl")

    async def add_referral(self, referral: str):
        return await self.fetch("PATCH", "users/me", {"referringUsername": referral})

    async def add_friend(self, id: str):
        return await self.fetch("POST", "friends/{}/requests".format(id))

    async def friend_status(self, id: str):
        return await self.fetch("GET", "friends/{}/status".format(id))

    async def remove_friend(self, id: str):
        return await self.fetch("DELETE", "friends/{}".format(id))

    async def accept_friend(self, id: str):
        return await self.fetch("PUT", "friends/{}/status".format(id), {"status": "ACCEPTED"})

    async def friend_list(self):
        return await self.fetch("GET", "friends")

    async def check_username(self, name: str):
        return await self.fetch("POST", "usernames/available", {"username": name})

    async def get_tokens(self, login_token: str):
        return await self.fetch("POST", "tokens", {'token': login_token})

    async def edit_username(self, username: str):
        return await self.fetch("PATCH", "users/me", {"username": username})

    async def get_login_token(self):
        return await self.fetch("GET", "users/me/token")

    async def send_documents(self, id, email, paypal_email, country):
        return await self.fetch("POST", "users/{}/payouts/documents".format(id),
                          {"email": email, "country": country, "payout": paypal_email})

    async def register_device_token(self, token):
        return await self.fetch("POST", "users/me/devices", {"token": token})

    async def config(self):
        return await self.fetch("GET", "config")

    async def get_optins(self):
        return await self.fetch("GET", "opt-in")

    async def set_optin(self, name: str, value: bool):
        return await self.fetch("POST", "opt-in", {"value": value, "opt": name})

    async def season_xp(self):
        return await self.fetch("GET", "seasonXp/settings")

    async def referrals(self):
        return await self.fetch("GET", "show-referrals")

    async def facebook_login(self, access_token):
        return await self.fetch("POST", "users/provider-auth", {"type":"FACEBOOK","token": access_token})

    async def google_login(self, jwt_token):
        return await self.fetch("POST", "users/provider-auth", {"type":"GOOGLE","token": jwt_token})

    async def swipe(self):
        return await self.fetch("POST", "easter-eggs/makeItRain")

    async def purchase_life(self, amount: int):
        return await self.fetch("POST", "store/com.intermedia.hq.item.extralife.{}x/purchase".format(amount))

    async def purchase_eraser(self, amount: int):
        return await self.fetch("POST", "store/com.intermedia.hq.item.erasers.{}x/purchase".format(amount))

    async def purchase_super_spin(self, amount: int):
        return await self.fetch("POST", "store/com.intermedia.hq.item.superspin.{}x/purchase".format(amount))

    async def leaderboard(self, mode: str):
        return await self.fetch("GET", "users/leaderboard?mode={}".format(mode))

    async def set_avatar(self, file: str):
        return await self.fetch("POST", "users/me/avatar", files={"file": ("file", open(file, 'rb').read(), 'image/jpeg')})

    async def store(self):
        return await self.fetch("GET", "store/products")

    async def start_offair(self):
        return await self.fetch('POST', "offair-trivia/start-game")

    async def offair_trivia(self, id: str):
        return await self.fetch('GET', 'offair-trivia/{}'.format(id))

    async def send_offair_answer(self, id: str, answer_id: str):
        return await self.fetch('POST', 'offair-trivia/{}/answers'.format(id), {"offairAnswerId": answer_id})

    async def custom(self, method, func, data):
        return await self.fetch(method, func, data)


class HQApi(BaseHQApi):
    def __init__(self, token: str = None, logintoken: str = None,
                 version: str = "1.39.0", host: str = "https://api-quiz.hype.space/",
                 proxy: str = None, verify: bool = True):
        super().__init__(token, logintoken)
        self.version = "2.4.3"
        self.session = requests.Session()
        self.token = token
        self.logintoken = logintoken
        self.hq_version = version
        self.host = host
        self.v = verify
        self.p = dict(http=proxy, https=proxy)
        self.headers = {
            "x-hq-client": "Android/" + self.hq_version}
        if logintoken:
            self.token = (await self.get_tokens(logintoken))["accessToken"]
        if self.token:
            self.headers["Authorization"] = "Bearer " + self.token

    async def fetch(self, method="GET", func="", data=None, files=None):
        if data is None:
            data = {}
        try:
            if method == "GET":
                content = self.session.get(self.host + "{}".format(func), data=data,
                                           headers=self.headers, proxies=self.p, verify=self.v).json()
            elif method == "POST":
                content = self.session.post(self.host + "{}".format(func), data=data,
                                            headers=self.headers, proxies=self.p, files=files, verify=self.v).json()
            elif method == "PATCH":
                content = self.session.patch(self.host + "{}".format(func), data=data,
                                             headers=self.headers, proxies=self.p, verify=self.v).json()
            elif method == "DELETE":
                content = self.session.delete(self.host + "{}".format(func), data=data,
                                              headers=self.headers, proxies=self.p, verify=self.v).json()
            elif method == "PUT":
                content = self.session.put(self.host + "{}".format(func), data=data,
                                           headers=self.headers, proxies=self.p, verify=self.v).json()
            else:
                content = self.session.get(self.host + "{}".format(func), data=data,
                                           headers=self.headers, proxies=self.p, verify=self.v).json()
            error = content.get("error")
            if error:
                raise ApiResponseError(json.dumps(content))
            return content
        except json.decoder.JSONDecodeError:
            raise BannedIPError("Your IP is banned")

    async def decode_jwt(self, jwt_text: str):
        return jwt.decode(jwt_text.encode(), verify=False)

    async def set_token(self, token):
        self.token = token
        if self.token:
            self.headers["Authorization"] = "Bearer " + self.token

    def __str__(self):
        return "<HQApi {} token={}>".format(self.version, self.token)
