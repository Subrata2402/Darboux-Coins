import websockets, aiohttp, re
import discord, requests, asyncio
from discord.ext import commands
from database import db
import aniso8601, json, threading
from bs4 import BeautifulSoup
from unidecode import unidecode
from datetime import datetime
from config import *
stored_ws = {}
question_number = total_question = 0
question = None

class HQWebSocket(object):
	
	def __init__(self, guild_id: int, client: commands.Bot):
		self.guild_id = guild_id
		self.client = client
		self.game_is_live = False
		self.demo_ws = "wss://hqecho.herokuapp.com"
		self.host = "https://api-quiz.hype.space"
		self.icon_url = "https://media.discordapp.net/attachments/799861610654728212/977325044097228870/49112C0D-6021-4333-9E6D-5E385EEE77E1-modified.png"
		self.socket_url = None
		self.answer_ids = None
		self.options = None
		self.pattern = []
	
	async def is_expired(self, token):
		"""Check either token is expired or not."""
		headers = {"Authorization": f"Bearer {token}"}
		async with aiohttp.ClientSession() as session:
			response = await session.get(self.host + "/users/me", headers = headers)
			if response.status != 200:
				await self.send_hook("The token has expired!")
				raise commands.CommandError("The token has expired")

	async def get_token(self):
		"""Take Authorization Bearer Token from the database for the different guild."""
		token = db.hq_details.find_one({"guild_id": self.guild_id})
		if not token:
			await self.send_hook("Please add HQ token to continue this process.")
			raise commands.CommandError("Token Not Found") # raise an exception if guild id not found in database
		token = token.get("token")
		await self.is_expired(token)
		return token

	async def get_ws(self):
		"""Get Websocket."""
		self.ws = stored_ws.get(self.guild_id)

	async def close_ws(self):
		"""Close Websocket."""
		await self.get_ws()
		if not self.ws:
			await self.send_hook("**Websocket Already Closed!**")
		else:
			if self.ws.closed:
				return await self.send_hook("**Websocket Already Closed!**")
			await self.ws.close()
			await self.send_hook("**Websocket Closed!**")

	async def get_web_url(self):
		"""Get discord channel Webhook url for different guild."""
		web_url = db.hq_details.find_one({"guild_id": self.guild_id})
		if not web_url:
			return web_url
		web_url = web_url.get("web_url")
		async with aiohttp.ClientSession() as session:
			response = await session.get(web_url)
			if response.status != 200:
				return None
		return web_url
		
	async def send_hook(self, content = "", embed = None):
		"""Send message with Discord channel Webhook."""
		web_url = await self.get_web_url()
		async with aiohttp.ClientSession() as session:
			webhook = discord.Webhook.from_url(web_url, adapter=discord.AsyncWebhookAdapter(session))
			await webhook.send(content = content, embed = embed, username = self.client.user.name, avatar_url = self.client.user.avatar_url)
			
	async def get_show_details(self, send_hook = None):
		"""Get show details of HQ Trivia."""
		async with aiohttp.ClientSession() as session:
			response = await session.get(self.host + "/shows/now")
			if response.status != 200:
				await self.send_hook("Something went wrong while fetching show details!")
				raise commands.CommandError("Show details not found")
			response_data = await response.json()
			time = response_data["nextShowTime"]
			tm = aniso8601.parse_datetime(time).timestamp()
			self.prize = response_data["nextShowPrize"]
			self.game_is_live = response_data['active']
			if self.game_is_live:
				self.socket_url = response_data['broadcast']['socketUrl'].replace('https', 'wss')
			if send_hook:
				embed = discord.Embed(color = discord.Colour.random())
				embed.title = "__Next Show Details !__"
				embed.description = f"Date : <t:{int(tm)}>\nPrize Money : {self.prize}"
				embed.set_thumbnail(url = self.icon_url)
				embed.set_footer(text = "HQ Trivia")
				embed.timestamp = datetime.utcnow()
				await self.send_hook(embed = embed)
			
	async def get_not_question(self, question) -> bool:
		"""Check either a question negative or not."""
		for negative_word in negative_words:
			if negative_word in question:
				not_question = True
				break
			else:
				not_question = False
		return not_question
		
	async def api_search_result(self, question, options, not_question) -> None:
		"""Get Google search results through the api."""
		url = 'https://jhatboyrahul.herokuapp.com/api/getResults'
		headers = {"Authorization": "RainBhai12"}
		payload = {'question': question, 'answer': options}
		async with aiohttp.ClientSession() as session:
			res = await session.post(url, headers = headers, json = payload)
			response = await res.json()
			count_options = dict(zip(options, response["data"]))
			max_count, min_count = max(response['data']), min(response["data"])
			min_max_count = min_count if not_question else max_count
			embed = discord.Embed(title=f"__Search Results -{order[2]}__", color = discord.Colour.random())
			embed.set_footer(text = "Display Trivia")
			embed.timestamp = datetime.utcnow()
			description = ""
			for index, option in enumerate(count_options):
				if max_count != 0 and count_options[option] == min_max_count:
					description += f"{order[index]}. {option} : {count_options[option]} ✅\n"
				else:
					description += f"{order[index]}. {option} : {count_options[option]}\n"
			embed.description = description
			await self.send_hook(embed = embed)
	
	async def rating_search_one(self, question_url, options, not_question) -> None:
		"""Get Google search results through rating."""
		r = requests.get(question_url)
		res = str(r.text).lower()
		count_options = {}
		for option in options:
			_option = replace_options.get(option)
			option = _option if _option else option
			count_option = res.count(option.lower())
			count_options[option] = count_option
		max_count = max(list(count_options.values()))
		min_count = min(list(count_options.values()))
		min_max_count = min_count if not_question else max_count
		embed = discord.Embed(title=f"__Search Results -{order[0]}__", color = discord.Colour.random())
		embed.set_footer(text = "Display Trivia")
		embed.timestamp = datetime.utcnow()
		description = ""
		for index, option in enumerate(count_options):
			if max_count != 0 and count_options[option] == min_max_count:
				description += f"{order[index]}. {option} : {count_options[option]} ✅\n"
			else:
				description += f"{order[index]}. {option} : {count_options[option]}\n"
		embed.description = description
		await self.send_hook(embed = embed)
	
	async def rating_search_two(self, question_url, choices, not_question) -> None:
		"""Get 2nd Google search results through rating."""
		r = requests.get(question_url)
		res = str(r.text).lower()
		count_options = {}
		for choice in choices:
			option = ""
			count_option = 0
			options = tuple(choice.split(" "))
			for opt in options:
				_option = replace_options.get(opt)
				opt = _option if _option else opt
				count = 0 if opt.lower() in ignore_options else res.count(opt.lower())
				count_option += count
				option += f"{opt}({count}) "
			count_options[option] = count_option
		max_count = max(list(count_options.values()))
		min_count = min(list(count_options.values()))
		min_max_count = min_count if not_question else max_count
		embed = discord.Embed(title=f"__Search Results -{order[1]}__", color = discord.Colour.random())
		embed.set_footer(text = "Display Trivia")
		embed.timestamp = datetime.utcnow()
		description = ""
		for index, option in enumerate(count_options):
			if max_count != 0 and count_options[option] == min_max_count:
				description += f"{order[index]}. {option}: {count_options[option]} ✅\n"
			else:
				description += f"{order[index]}. {option}: {count_options[option]}\n"
		embed.description = description
		if max_count != 0: await self.send_hook(embed = embed)
	
	async def direct_search_result(self, question_url, options):
		"""Get Direct google search results."""
		r = requests.get(question_url)
		soup = BeautifulSoup(r.text , "html.parser")
		response = soup.find("div" , class_='BNeawe')
		result = str(response.text)
		embed = discord.Embed(
			description = result,
			color = discord.Colour.random(),
			timestamp = datetime.utcnow()
			)
		embed.set_footer(text="Search with Google")
		option_found = False
		for index, option in enumerate(options):
			if option.lower().strip() in result.lower():
				embed.title = f"__Option {order[index]}. {option}__"
				embed.description = re.sub(f'{option.strip()}', f'**__{option}__**', result, flags = re.IGNORECASE)
				option_found = True
		if not option_found:
			embed.title = f"__Direct Search Result !__"
		await self.send_hook(embed = embed)
			
	async def connect_ws(self, demo = None):
		"""Connect websocket."""
		token = await self.get_token()
		await self.is_expired(token)
		await self.get_show_details()
		if not self.game_is_live:
			await self.send_hook("Game is not live!")
			raise commands.CommandError("Game is not live")
		headers = {
			"Authorization": f"Bearer {token}",
			"x-hq-client": "iPhone8,2"
		}
		try:
			self.ws = await websockets.connect(self.socket_url, extra_headers = headers, ping_interval = 15)
		except Exception as e:
			print(e)
			return await self.send_hook("Something went wrong while creating the connection.")
		stored_ws[self.guild_id] = self.ws
		async for message in self.ws:
			message_data = json.loads(message)
			#await self.send_hook(f"```\n{message_data}\n```")
			if message_data['type'] == 'gameStatus':
				await self.send_hook("Websocket Successfully Connected!")
				log_channel = self.client.get_channel(967462642723733505) or (await self.client.fetch_channel(967462642723733505))
				guild = self.client.get_guild(self.guild_id) or (await self.client.fetch_guild(self.guild_id))
				await log_channel.send(f"HQ Trivia Bot started in {guild.name}!")
			
			elif message_data['type'] == 'interaction':
				pass
			
			elif message_data['type'] == 'question':
				global question_number, total_question, question
				question = message_data['question']
				question_number = message_data['questionNumber']
				total_question = message_data['questionCount']
				self.options = [unidecode(ans["text"].strip()) for ans in message_data["answers"]]
				self.answer_ids = [ans["answerId"] for ans in message_data["answers"]]
				raw_question = str(question).replace(" ", "+")
				google_question = "https://google.com/search?q=" + raw_question
				u_options = "+or+".join(self.options)
				raw_options = str(u_options).replace(" ", "+")
				search_with_all = "https://google.com/search?q=" + raw_question + "+" + raw_options
				not_question = await self.get_not_question(question.lower())
				is_not = "(Not Question)" if not_question else ""
		
				embed = discord.Embed(color = discord.Colour.random())
				embed.title = f"Question {question_number} out of {total_question} {is_not}"
				embed.description = f"[{question}]({google_question})\n\n[Search with all options]({search_with_all})"
				for index, option in enumerate(self.options):
					embed.add_field(name = f"Option - {order[index]}", value = f"[{option.strip()}]({google_question + '+' + str(option).strip().replace(' ', '+')})", inline = False)
				embed.set_footer(text = "HQ Trivia")
				embed.set_thumbnail(url = self.icon_url)
				embed.timestamp = datetime.utcnow()
				await self.send_hook(embed = embed)
				
				target_list = [
						self.rating_search_one(google_question, self.options, not_question),
						self.rating_search_two(google_question, self.options, not_question),
						self.api_search_result(question, self.options, not_question),
						self.direct_search_result(google_question, self.options),
					]
						#self.direct_search_result(search_with_all, choices)
				for target in target_list:
					thread = threading.Thread(target = lambda: asyncio.run(target))
					thread.start()
					
			elif message_data['type'] == 'answered':
				username = message_data["username"]
				ans_id = message_data["answerId"]
				for index, answer_id in enumerate(self.answer_ids):
					if ans_id == answer_id:
						option = self.options[index]
						embed = discord.Embed(color = discord.Colour.random())
						embed.title = f"__{username}__"
						embed.description = f"Option {order[index]}. {option}"
						await self.send_hook(embed = embed)
			
			elif message_data["type"] == "questionClosed":
				embed = discord.Embed(title = "⏰ | Time's Up!", color = discord.Colour.random())
				await self.send_hook(embed = embed)
				
			elif message_data["type"] == "questionSummary":
				for index, answer in enumerate(message_data["answerCounts"]):
					if answer["correct"]:
						option = answer["answer"]
						ans_num = index + 1
				self.pattern.append(str(ans_num))
				advance_players = message_data['advancingPlayersCount']
				eliminate_players = message_data['eliminatedPlayersCount']
				ans = 1500/advance_players
				payout = float("{:.2f}".format(ans))
				total_players = advance_players + eliminate_players
				percentAdvancing = (advance_players*100)/total_players
				pA = float("{:.2f}".format(percentAdvancing))
				percentEliminated = (eliminate_players*100)/total_players
				pE = float("{:.2f}".format(percentEliminated))
			
				embed = discord.Embed(
					title = f"Question {question_number} out of {total_question}",
					description = f"[{question}]({google_question})",
					color = discord.Colour.random(),
					timestamp = datetime.utcnow()
					)
				embed.add_field(name = "Correct Answer :-", value = f"Option {order[ans_num-1]}. {option}", inline = False)
				embed.add_field(name = "Status :-",
					value = f"Advancing Players : {advance_players} ({pA}%)\nEliminated Players : {eliminate_players} ({pE}%)\nCurrent Payout : ${payout}",
					inline = False
				)
				embed.add_field(name = "Ongoing Pattern :-", value = f"{self.pattern}", inline = False)
				embed.set_footer(text = "HQ Trivia")
				embed.set_thumbnail(url = self.icon_url)
				await self.send_hook(embed = embed)
				
			elif message_data["type"] == "gameSummary":
				winn = message_data['numWinners']
				prizeMoney = str(message_data["winners"][0]["prize"])
				embed=discord.Embed(title = "__Game Summary !__",description = f"● Payout : {prizeMoney}\n● Total Winners : {winn}\n● Prize Money : {self.prize}", color = discord.Colour.random())
				embed.set_thumbnail(url = self.icon_url)
				embed.set_footer(text = "HQ Trivia")
				embed.timestamp = datetime.utcnow()
				await self.send_hook(embed = embed)
				self.pattern.clear()
				await self.close_ws()
