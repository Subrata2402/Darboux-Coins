import json, jwt, requests
from HQApi.exceptions import ApiResponseError, BannedIPError

class BaseHQApi:
    def __init__(self, token: str = None, logintoken: str = None):
        self.token = token
        self.logintoken = logintoken

    async def api(self):
        return self

    async def get_users_me(self):
        """response_data = {
                    'achievementCount': 0,
                    'avatarUrl': 'https://cdn.prod.hype.space/da/gold.png',
                    'blocked': False,
                    'blocksMe': False,
                    'broadcasts': {'data': []},
                    'coins': 678,
                    'created': '2021-03-23T02:35:38.000Z',
                    'deviceTokens': [],
                    'erase1s': 0,
                    'featured': False,
                    'friendIds': [],
                    'gamesPlayed': 12,
                    'hasPhone': True,
                    'highScore': 0,
                    'identities': [],
                    'items': {'erase1s': 0, 'lives': 2, 'popularChoices': None, 'superSpins': 0},
                    'leaderboard': {
                                'alltime': {'rank': 101, 'total': '$0', 'wins': 0},
                                'rank': 101,
                                'total': '$0',
                                'totalCents': 0,
                                'unclaimed': '$0',
                                'weekly': {'rank': 101, 'total': '$0', 'wins': 0},
                                'wins': 0
                    },
                    'lives': 2,
                    'phoneNumber': '+447404447991',
                    'preferences': {'hq-general': True, 'sharingEnabled': True},
                    'referralUrl': 'https://hqtrivia.com/i/HelmaKai95',
                    'referred': True,
                    'referringUserId': 27015094,
                    'stk': 'Mg==',
                    'streakInfo': {
                            'current': 0,
                            'lastPlayed': '2022-03-28T21:40:42.327Z',
                            'lifeUuid': None,
                            'notify': True,
                            'startDate': '2022-03-28T07:00:00.000Z',
                            'target': 5,
                            'total': 0,
                            'userId': 27353247
                    },
                    'userId': 27353247,
                    'username': 'HelmaKai95',
                    'voip': False,
                    'winCount': 0
                }"""
        return await self.fetch("GET", "users/me")

    async def get_user(self, id: str):
        return await self.fetch("GET", "users/{}".format(id))

    async def search(self, name):
        """response_data = {
            'data': [{
                'avatarUrl': 'https://cdn.prod.hype.space/da/purple.png',
                'created': '2020-06-02T02:41:50.000Z',
                'featured': False,
                'lastLive': None,
                'live': False,
                'subscriberCount': 0,
                'userId': '26755116',
                'username': 'josephine3250'
            },
            {
                'avatarUrl': 'https://cdn.prod.hype.space/da/blue.png',
                'created': '2021-05-24T06:07:00.000Z',
                'featured': False,
                'lastLive': None,
                'live': False,
                'subscriberCount': 0,
                'userId': '27480572',
                'username': 'Josephine3250fb'
            }],
            'links': {
                'next': None,
                'prev': '/users?q=Josephine3250&before=1',
                'self': '/users?q=Josephine3250'
                }
            }"""
        return await self.fetch("GET", 'users?q={}'.format(name))

    async def get_payouts_me(self):
        """response_data = {
                    'balance': {
                        'appealStatus': 'none',
                        'available': '$0',
                        'documentRequired': False,
                        'documentStatus': 'none',
                        'eligibleForPayout': False,
                        'frozen': '$0',
                        'hasPending': False,
                        'paid': '$10.50',
                        'payoutEligibility': 'disallowed_not_enough',
                        'payoutsConnected': True,
                        'payoutsEmail': 'sakhman2001@gmail.com',
                        'pending': '$0',
                        'prizeTotal': '$10.50',
                        'unpaid': '$0',
                        'winsReadyForCashout': True
                    },
                    'charities': [{
                        'charityIconUrl': 'https://cdn.prod.hype.space/charity-icons/7692404-A1IHqy',
                        'charityId': 'ckfbjy9qp0000015a2u78gl3k',
                        'displayName': "Tuesday's Children"
                    },
                    {
                        'charityIconUrl': 'https://cdn.prod.hype.space/charity-icons/7692404-mkzp4p',
                        'charityId': 'ckfbjxf7d0000011ubxtq2s6p',
                        'displayName': 'Rock the Vote'
                    }],
                    'payouts': [{
                        'amount': '$1.88',
                        'created': '2021-05-03T01:43:02.000Z',
                        'currency': 'USD',
                        'metadata': {
                                'batchId': 'KC2ZUQES5NTKE',
                                'client': 'Android/1.49.8',
                                'ipAddress': '54.242.1.233',
                                'payoutsConnected': True,
                                'senderBatchId': 'payout_4827411'
                            },
                        'modified': '2021-05-03T01:47:59.000Z',
                        'payoutId': 4827411,
                        'status': 10001,
                        'targetEmail': 'sakhman2001@gmail.com',
                        'targetPhone': None,
                        'targetUserId': None,
                        'userId': 27232225
                    },
                    {
                        'amount': '$0.79',
                        'created': '2021-04-07T03:03:47.000Z',
                        'currency': 'USD',
                        'metadata': {
                                'batchId': '88ULYQXB74SME',
                                'client': 'Android/1.49.8',
                                'ipAddress': '35.175.205.12',
                                'payoutsConnected': True,
                                'senderBatchId': 'payout_4815149'
                            },
                        'modified': '2021-04-13T16:26:17.000Z',
                        'payoutId': 4815149,
                        'status': 10001,
                        'targetEmail': 'sakhman2001@gmail.com',
                        'targetPhone': None,
                        'targetUserId': None,
                        'userId': 27232225
                    },
                ]}"""
        return await self.fetch("GET", "users/me/payouts")

    async def get_show(self):
        """response_data = {
                    'active': False,
                    'atCapacity': False,
                    'broadcast': None,
                    'broadcastFull': False,
                    'gameType': None,
                    'media': None,
                    'nextGameType': 'trivia',
                    'nextShowPrize': '$1,500',
                    'nextShowTime': '2022-04-01T01:00:00.000Z',
                    'nextShowVertical': 'general',
                    'prize': None,
                    'prizePoints': None,
                    'showId': None,
                    'showType': None,
                    'startTime': None,
                    'upcoming': [{
                            'gameType': 'trivia',
                            'media': [],
                            'nextShowLabel': {'color': '#FFFFFF', 'title': 'HQ Trivia'},
                            'optIn': {'color': '#FFFFFF', 'opt': 'hq-general'},
                            'prize': '$1,500',
                            'showType': 'hq',
                            'time': '2022-04-01T01:00:00.000Z',
                            'vertical': 'general'}
                        ]}"""
        return await self.fetch("GET", "shows/now")

    async def get_schedule(self):
        """response_data = {
                    'announcements': [],
                    'offairTrivia': {
                                'games': [{
                                    'answerResults': [True],
                                    'category': 'TV',
                                    'gameUuid': 'cl17nlnqc07vx01i98jpjfr3b',
                                    'questionCount': 12,
                                    'questionNumber': 2,
                                    'reminders': [{
                                            'message': 'Complete your Daily '
                                                        'Challenge now before '
                                                        'it’s too late!',
                                            'sendMs': 14400000}],
                                    'status': 'question_answered'}],
                                'isGameInProgress': True,
                                'powerups': {
                                    'OFFAIR_PTS_MULTI_10': 0,
                                    'OFFAIR_UNLOCK': 0,
                                    'offair-10x-pts-multi': 0,
                                    'offair-unlock': 0},
                                'waitTimeMs': 0},
                    'shows': [{
                        'currency': 'USD',
                        'display': {
                            'accentColor': '#FFFFFF',
                            'bgImage': 'https://cdn.prod.hype.space/static/channel/TRIVIA/Trivia-frame.png',
                            'bgVideo': 'https://cdn.prod.hype.space/static/channel/TRIVIA/HQ-Trivia-portrait-70percentSpeed-190kbps-HVEC_H265.mp4',
                            'description': 'Are you a sponge of random facts? HQ '
                                           'Trivia is the viral hit live mobile '
                                           'game show where your trivia smarts '
                                           'helps you win real cash. Answer '
                                           'questions that range from easy to '
                                           'hard, and if you get them all right, '
                                           'you win or split the cash prize.',
                            'image': 'https://cdn.prod.hype.space/static/channel/TRIVIA/Trivia@3x.png?v=3',
                            'logo': 'https://cdn.prod.hype.space/static/channel/TRIVIA/Trivia@3x.png?v=3',
                            'subtitle': '$1,500 Prize!',
                            'summary': 'Answer trivia for cash prizes',
                            'title': 'HQ Trivia'},
                        'gameType': 'trivia',
                        'media': [],
                        'opt': 'hq-general',
                        'prizeCents': 150000,
                        'showId': 15077,
                        'showType': 'hq',
                        'startTime': '2022-04-01T01:00:00.000Z',
                        'vertical': 'general'}]}"""
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
        response_data = {
                    'coinsPurchased': 0,
                    'coinsTotal': 24562,
                    'itemsPurchased': {'extra-life': 1},
                    'itemsTotal': {'extra-life': 2, 'super-spin': 2},
                    'subscriptions': [],
                    'transactionId': None
                }
        return await self.fetch("POST", "store/com.intermedia.hq.item.extralife.{}x/purchase".format(amount))

    async def purchase_eraser(self, amount: int):
        response_data = {
                    'coinsPurchased': 0,
                    'coinsTotal': 24462,
                    'itemsPurchased': {'eraser': 1},
                    'itemsTotal': {'eraser': 1, 'extra-life': 2, 'super-spin': 2},
                    'subscriptions': [],
                    'transactionId': None
                }
        return await self.fetch("POST", "store/com.intermedia.hq.item.erasers.{}x/purchase".format(amount))

    async def purchase_super_spin(self, amount: int):
        response_data = {
                    'coinsPurchased': 0,
                    'coinsTotal': 24312,
                    'itemsPurchased': {'super-spin': 1},
                    'itemsTotal': {'eraser': 1, 'extra-life': 2, 'super-spin': 3},
                    'subscriptions': [],
                    'transactionId': None
                }
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
            self.token = self.get_tokens(logintoken)["accessToken"]
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
                raise ApiResponseError(error)
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
