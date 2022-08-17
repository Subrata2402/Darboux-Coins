import discord
from Websocket.swagbucks_ws import SbWebSocket, SwagbucksLive
from discord.ext import commands
from database import db
import threading, asyncio

class SwagbucksTrivia(commands.Cog, SwagbucksLive):
	
	def __init__(self, client):
		super().__init__(client)
		self.client = client

	async def start(self, ctx, username: str):
		ws = SbWebSocket(self.client, username)
		await ws.get_ws()
		if ws.ws:
			if ws.ws.open:
				return await ws.send_hook("Websocket Already Opened!")
		await ws.send_hook("Websocket Connecting...")
		await ws.connect_websocket(ctx.channel.id, ctx.author.id)

	@commands.command()
	@commands.is_owner()
	async def sbstart(self, ctx, username: str = None):
		"""
		Check and open a websocket by username.
		"""
		if ctx.channel.id != 1009531267739557939: return
		# if not username:
		#	return await ctx.send("username is required!")
		# if username == "all":
		# details = list(db.sb_details.find())
		# for data in details:
		# # 		if data["username"] == "subrata3250": continue
		# 	thread = threading.Thread(target = lambda: asyncio.run(self.start(ctx, data["username"])))
		# 	thread.start()
		# else:
		await self.start(ctx, username)
		
		
	@commands.command()
	@commands.is_owner()
	async def sbclose(self, ctx, username: str = None):
		"""
		Close a websocket by username.
		"""
		if ctx.channel.id != 1009531267739557939: return
		ws = SbWebSocket(self.client, username.lower())
		await ws.close_ws()
	
	@commands.command()
	@commands.is_owner()
	async def sblogin(self, ctx, email_id: str = None, password: str = None):
		"""
		Login a Swagbucks account and stored some required details in the database.
		"""
		if ctx.channel.id != 1009531267739557939: return

		if not email_id or not password:
			return await ctx.send("Username or Password is required to login to Swagbucks.")
		await self.login(email_id, password)
		
	@commands.command()
	@commands.is_owner()
	async def sbupdate(self, ctx, username: str = None):
		"""
		If account is expire then this command will delete the stored account details
		and login again to update account.
		"""
		if ctx.channel.id != 1009531267739557939: return

		if not username:
			return await ctx.send("Required username to update of Swagbucks account.")
		await self.update_account(username)
		
	@commands.command()
	@commands.is_owner()
	async def sbdetails(self, ctx, username: str = None):
		"""
		Get stats details of a Swagbucks account.
		"""
		if ctx.channel.id != 1009531267739557939: return

		if not username:
			return await ctx.send("Required username to get details of Swagbucks account.")
		await self.account_details(username.lower())
		
	
	@commands.command()
	@commands.is_owner()
	async def sbaccounts(self, ctx):
		"""
		Get all accounts username, stored in the database.
		"""
		if ctx.channel.id != 1009531267739557939: return

		accounts = list(db.sb_details.find())
		description = ""
		for index, data in enumerate(accounts):
			description += "{}{} - {}\n".format(0 if index+1 < 10 else "", index+1, data["username"])
		if not accounts:
			return await ctx.send("No accounts found.")
		await ctx.send("```\n{}\n```".format(description))
		
	@commands.command()
	@commands.is_owner()
	async def sbbal(self, ctx):
		"""
		Get all accounts Swagbucks details, stored in the database.
		"""
		if ctx.channel.id != 1009531267739557939: return

		accounts = list(db.sb_details.find())
		description = ""
		for index, data in enumerate(accounts):
			sb = await self.account_details(data["username"].lower(), True)
			description += "{}{} - {} - {} SB\n".format(0 if index+1 < 10 else "", index+1, data["username"], sb)
		if not accounts:
			return await ctx.send("No accounts found.")
		await ctx.send("```\n{}\n```".format(description))
    
		
	@commands.command()
	@commands.is_owner()
	async def sbnextshow(self, ctx):
		"""
		Get Swagbucks Live next show details.
		"""
		if ctx.channel.id != 1009531267739557939: return

		username = list(db.sb_details.find())[0]["username"]
		ws = SwagbucksLive(self.client, username)
		await ws.show_details()
		
	# @commands.command()
	# async def sbtoken(self, ctx, email_id: str = None, password: str = None):
	# 	if ctx.guild:
	# 		return await ctx.send("Please use this command in Private Messages.")
	# 	if not email_id or not password:
	# 		return await ctx.send("Username or Password is required to login to Swagbucks.")
	# 	token = await self.login(email_id, password, "GET")
	# 	await ctx.send("```\n{}\n```".format(token))
		
def setup(client):
	client.add_cog(SwagbucksTrivia(client))
