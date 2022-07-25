import aiohttp, json, discord
stored_ws = {}
from datetime import datetime
import websockets, asyncio, requests
from database import db

signed = {
	"josephine325": "cf737f54a923ae5f300a705332352e3a",
	"baldric3250schne": "172e4aebc29f853bb8033a987d470837",
	"subrata3250": "a516124913fb217d2f8b2d3dfe661950",
	"baldric3250": "fdd68b74901e530ac2306d3ba3d88edb",
	"sakhman2001sdas": "29e8b38bb30e13f93d09a71ae273a3b6",
	"bernfried3250": "4fc4ccb673ca83b52d5979d3eb5f130a",
	"bernfried32": "21a8cfa770c81bd5f9c024a20ee36ac7",
	"sakhman32": "ecc1a1ee7fa28ab8ee2be273de04ae7c",
	"kamal3085": "d9a3583b33ccd0f070d9cb343690a3c6",
	"kmidya1233": "ef8db1cbccfdc6b2b12d2ecb99d0b46f"
}

class SbWebSocket(object):
	
	def __init__(self, client, username: str = None):
		self.client = client
		self.username = username if username else "User"
		self.ws = None # websocket 
		self.vid = None # current game view id or video id
		self.game_is_active = False # game is live or not
		self.answer = 2
		self.data = None # send answer data
		self.game_id = None # 1254
		self.note = None # 2022-07-06 5:00pm PT
		self.host = "https://api.playswagiq.com/"
		self._host = "https://app.swagbucks.com/"
		self.icon_url = "https://cdn.discordapp.com/attachments/799861610654728212/991317134930092042/swagbucks_logo.png"
		self.headers = {
			"content-type": "application/x-www-form-urlencoded",
			"Host": "api.playswagiq.com",
			"user-agent": "SwagIQ-Android/34 (okhttp/3.10.0)",
			"accept-encoding": "gzip",
			"authorization": "Bearer " + self.get_token()
		}
		
	async def is_expired(self):
		"""
		Check if an account is expired and delete it from the database.
		And login again to update the account.
		"""
		data = await self.fetch("POST", "trivia/home", headers = self.headers)
		success = data["success"]
		if not success:
			return await self.send_hook("Auth token has expired!")
		
	def get_token(self):
		"""
		Get token from database by username.
		"""
		details = db.sb_details.find_one({"username": self.username.lower()})
		if not details:
			print("Not Found any account with this username")
			return "gkdykludkeouflud"
		return details["access_token"]
		
	async def game_details(self) -> None:
		"""
		Get game details.
		"""
		data = await self.fetch("POST", "trivia/join", headers = self.headers)
		if data["success"]:
			self.game_is_active = True
			self.vid = data["viewId"]
			self.game_id = data["episode"]["id"]
			self.note = data["episode"]["title"]
	
	async def get_partner_hash(self, question_number: str):
		"""
		Get partner hash for confirmation of rejoin in the live game.
		"""
		user_details = db.sb_details.find_one({"username": self.username.lower()})
		token = user_details["token"]
		params = {
			"token": token, "gameID": str(self.game_id),
			"price": "0", "questionNumber": question_number,
			"note": self.note, "useLife": "true", "appid": "37",
			"appversion": "34", "sig": signed[self.username],
		}
		# post_data = f"token={token}&gameID={str(self.game_id)}&price=0&questionNumber={question_number}&note={self.note}&useLife=true&appid=37&appversion=34&sig={signed[self.username]}"
		headers = {
			"content-type": "application/x-www-form-urlencoded",
			"Host": "app.swagbucks.com",
			"user-agent": "SwagIQ-Android/34 (okhttp/3.10.0);Realme RMX1911",
			"accept-encoding": "gzip",
		}
		data = await self.fetch("POST", "?cmd=apm-70", headers = headers, params = params, host = "host")
		await self.send_hook("\n```\n{}\n```".format(data))
		return data.get("sig")

	
	async def fetch(self, method = "GET", function = "", headers = None, params = None, data = None, host = None):
		"""
		Request Swagbucks to perform the action.
		"""
		host = self._host if host else self.host
		async with aiohttp.ClientSession() as client_session:
			response = await client_session.request(method = method, url = host + function, params = params, headers = headers, data = data)
			content = await response.text()
			return json.loads(content)
	
	async def send_answer(self, qid: str, aid: str) -> None:
		"""
		Send answer to the game.
		"""
		params = {
			"vid": self.vid, "qid": qid, "aid": aid, "timeDelta": "5000"
		}
		self.data = await self.fetch("POST", "trivia/answer", headers = self.headers, params = params)
		await self.send_hook("\n```\n{}\n```".format(self.data))
	
	async def confirm_rebuy(self, question_number: str) -> None:
		"""
		If any question is wrong then we are eliminated.
		For come back and join again to the game we use a rejoin.
		To use this function we can send a rejoin. 
		"""
		if self.data.get("whenIncorrect"):
			allow_rebuy = self.data["whenIncorrect"]["allowRebuy"]
		else:
			return None
		# params = {
		# 	"vid": self.vid, "useLife": "true", "partnerHash": self.partner_hash,
		# 	#"_device": "c1cd7fc0-4bd5-4026-bc7d-aaa4199b7873"
		# }
		if allow_rebuy:
			partner_hash = await self.get_partner_hash(question_number)
			if not partner_hash: return 
			post_data = f"vid={self.vid}&useLife=true&partnerHash={partner_hash}"
			data = await self.fetch("POST", "trivia/rebuy_confirm", headers = self.headers, data = post_data)
			await self.send_hook("\n```\n{}\n```".format(data))
			
	async def confirm_sb(self) -> None:
		"""
		If lost the game, Swagbucks asked to confirm to take bonus sb.
		Then you need confirm sb to credited sb in Swagbucks wallet.
		"""
		# params = {
		# 	"vid": self.vid, "useLife": "true", "partnerHash": self.partner_hash,
		# 	#"_device": "c1cd7fc0-4bd5-4026-bc7d-aaa4199b7873"
		# }
		
		post_data = f"vid={self.vid}"
		data = await self.fetch("POST", "trivia/confirm_sb", headers = self.headers, data = post_data)
		await self.send_hook("\n```\n{}\n```".format(data))
	
	async def complete_game(self) -> None:
		"""
		After end of the game check the details of winnings 
		and how many sb earn from the live game.
		"""
		# params = {"vid": self.vid}
		post_data = f"vid={self.vid}"
		data = await self.fetch("POST", "trivia/complete", headers = self.headers, data = post_data)
		# success = data.get("success")
		# if success:
		# 	await self.send_hook("Successfully complete the game.")
		# 	winner = data.get("winner")
		# 	sb = data.get("sb")
		# 	await self.send_hook("You **{}** the game and got **{} SB**!".format('won' if winner else 'lost', sb))
		# else:
		# 	await self.send_hook("Failed to complete the game.\n```\n{}\n```".format(data))
		await self.send_hook("\n```\n{}\n```".format(data))
		
		confirm = data["confirm"]
		winner = data["winner"]
		if confirm and not winner:
			await self.confirm_sb()
			# await self.send_hook("\n```\n{}\n```".format(data))

	
	async def get_ws(self) -> None:
		"""
		Get Websocket.
		"""
		self.ws = stored_ws.get(self.username)

	async def close_ws(self) -> None:
		"""
		Close Websocket.
		"""
		await self.get_ws()
		if not self.ws:
			await self.send_hook("**Websocket Already Closed!**")
		else:
			if self.ws.closed:
				return await self.send_hook("**Websocket Already Closed!**")
			await self.ws.close()
			await self.send_hook("**Websocket Closed!**")
			
	async def send_hook(self, content = "", embed = None) -> None:
		"""
		Send message with Discord channel Webhook.
		"""
		web_url = "https://discord.com/api/webhooks/988392404853874748/CGtvuLqXpX4kTuWJrV6KsTkPjXowVJRrcFk_rWKVLlJuZFQpNU7lIPWOm4UpKupKqU7T"
		async with aiohttp.ClientSession() as session:
			webhook = discord.Webhook.from_url(web_url, adapter=discord.AsyncWebhookAdapter(session))
			await webhook.send(content = content, embed = embed, username = self.client.user.name, avatar_url = self.client.user.avatar_url)
			
	
	async def connect_websocket(self, channel_id: int, author_id: int):
		"""
		Connect websocket to join Swagbucks Live game and play.
		"""
		await self.is_expired()
		await self.game_details()
		if not self.game_is_active:
			return await self.send_hook("Game is not live!")
		socket_url = "wss://api.playswagiq.com/sock/1/game/{}".format(self.vid)
		self.ws = await websockets.connect(socket_url, extra_headers = self.headers, ping_interval = 15)
		stored_ws[self.username] = self.ws
		question_number = 0
		await self.send_hook("Websocket successfully connected!")
		async for message in self.ws:
			message_data = json.loads(message)
			if message_data["code"] == 41:
				question_number = message_data["question"]["number"]
				total_question = message_data["question"]["totalQuestions"]
				question_id = message_data["question"]["idSigned"]
				answer_ids = [answer["idSigned"] for answer in message_data["question"]["answers"]]
				
				embed = discord.Embed(title = f"Question {question_number} out of {total_question}", url = "https://google.com")
				await self.send_hook(embed = embed)
				def check(message):
					return message.channel.id == channel_id and message.author.id == author_id
				try:
					user_input = await self.client.wait_for("message", timeout = 11.0, check = check)
					self.answer = int(user_input.content.strip())
				except Exception as e:
					await self.send_hook("You failed to send your answer within time or something went wrong.\n```\n{}\n```".format(e))
				answer_id = answer_ids[self.answer - 1]
				await self.send_answer(question_id, answer_id)
					
			if message_data["code"] == 42:
				ansid = message_data["correctAnswerId"]
				for index, answer in enumerate(message_data["answerResults"]):
					if answer["answerId"] == ansid:
						ans_num = index + 1
				
				embed = discord.Embed(title = f"Correct Answer : {ans_num}")
				await self.send_hook(embed = embed)
				
				if self.answer != ans_num:
					await self.confirm_rebuy(str(question_number))
					
			if message_data["code"] == 49:
				await self.complete_game()
				await self.close_ws()
				
class SwagbucksLive(SbWebSocket):
	
	def __init__(self, client, username: str = None):
		super().__init__(client, username)
		self.client = client

	async def login(self, email_id: str, password: str, get_token: str = None):
		"""
		Login to Swagbucks with username and password
		and save login credentials to database.
		"""
		params = {
			"emailAddress": email_id,
			"pswd": password,
			# "persist": "on", "showmeter": "0",
			"sig": signed[email_id],
			# "advertiserID": "e1cbd4d6-3aea-4144-82b9-2a70b8458f5b",
			# "modelNumber": "RMX1911829", "osVersion": "10",
			"appversion": "34",
			"appid": "37"
		}
		headers = {
			"content-type": "application/x-www-form-urlencoded",
			"Host": "app.swagbucks.com",
			"user-agent": "SwagIQ-Android/34 (okhttp/3.10.0);Realme RMX1911",
			"accept-encoding": "gzip",
			# "authorization": self.get_token()
		}
		data = await self.fetch("POST", "?cmd=apm-1", headers = headers, params = params, host = "host")
		if data["status"] != 200:
			return await self.send_hook("```\n{}\n```".format(data))
		username = data["user_name"]
		user_id = data["member_id"]
		check = db.sb_details.find_one({"user_id": user_id})
		if check: return await self.send_hook("This account already exists in bot.")
		token = data["token"]
		sig = data["sig"]
		
		# params = {
		# 	"_device": "c1cd7fc0-4bd5-4026-bc7d-aaa4199b7873",
		# 	"partnerMemberId": user_id,
		# 	"partnerUserName": username,
		# 	"verify": "false",
		# 	"partnerApim": "1",
		# 	"partnerHash": sig
		# }
		
		data = f"_device=f6acc085-c395-4688-913f-ea2b36d4205f&partnerMemberId={user_id}&partnerUserName={username}&verify=false&partnerApim=1&partnerHash={sig}"
		data = await self.fetch("POST", "auth/token", headers = headers, data = data)
		access_token = data["accessToken"]
		refresh_token = data["refreshToken"]
		if get_token: return access_token
		db.sb_details.insert_one({
			"user_id": user_id, "username": username.lower(),
			"access_token": access_token, "refresh_token": refresh_token,
			"token": token, "sig": sig,
			"email_id": email_id, "password": password
		})
		await self.send_hook("Successfully login to Swagbucks. Username : `{}`".format(username))
	
	async def account_details(self, username: str, sb: bool = False):
		"""
		Get account details.
		"""
		user_details = db.sb_details.find_one({"username": username.lower()})
		if not user_details:
			return await self.send_hook("No account found with name `{}`".format(username))
		token = user_details["token"]
		params = {
			"token": token, "checkreferral": "false",
			"appid": "37", "appversion": "34"
		}
		headers = {
			"content-type": "application/x-www-form-urlencoded",
			"Host": "app.swagbucks.com",
			"user-agent": "SwagIQ-Android/34 (okhttp/3.10.0);Realme RMX1911",
			"accept-encoding": "gzip",
			# "authorization": self.get_token()
		}
		data = await self.fetch("POST", "?cmd=apm-3", headers = headers, params = params, host = "host")
		if data["status"] != 200:
			return await self.send_hook("```\n{}\n```".format(data))
		if sb: return data["swagbucks"]
		description = f"```\n" \
				f"• User Id             ::  {data['member_id']}\n" \
				f"• Email Verified      ::  {data['email_verified']}\n" \
				f"• Rejoins (Lives)     ::  {data['lives']}\n" \
				f"• Username            ::  {data['user_name']}\n" \
				f"• Swagbucks (SB)      ::  {data['swagbucks']}\n" \
				f"• Re-Verification     ::  {data['require_reverification']}\n" \
				f"• Profile Complete    ::  {data['profile_complete']}\n" \
				f"• OTP Verified        ::  {data['otp_verified']}\n" \
				f"• Member Status       ::  {data['member_status']}\n" \
				f"• Pending Earnings    ::  {data['pending_earnings']}\n" \
				f"• Registered Date     ::  {data['registered_date']}\n" \
				f"• Lifetime Earnings   ::  {data['lifetime_earnings']}\n```"
		await self.send_hook(description)
		
	async def show_details(self) -> None:
		"""
		Get the details of the current game show.
		"""
		await self.is_expired()
		data = await self.fetch("POST", "trivia/home", headers = self.headers)
		prize = data["episode"]["grandPrizeDollars"]
		time = data["episode"]["start"]
		embed=discord.Embed(title = "__SwagIQ Next Show Details !__", description=f"• Show Name : Swagbucks Live\n• Show Time : <t:{time}>\n• Prize Money : ${prize}", color = discord.Colour.random())
		embed.set_thumbnail(url = self.icon_url)
		embed.set_footer(text = "Swagbucks Live")
		embed.timestamp = datetime.utcnow()
		await self.send_hook(embed = embed)
