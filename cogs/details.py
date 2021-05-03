import discord
import random
from discord.ext import commands
import asyncio
from pymongo import MongoClient
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from HQApi import HQApi, HQWebSocket
import asyncio
from datetime import datetime
import requests
import json
import time
import colorsys
import datetime
import aniso8601
from pytz import timezone
from unidecode import unidecode
from bs4 import BeautifulSoup

data = MongoClient('mongodb+srv://Subrata2001:Subrata2001@cluster0.ywnwn.mongodb.net/Darboux?retryWrites=true&w=majority')#Your Database Url
db = data.get_database("Darboux")#Your db name
token_base = db.token
login_token_base = db.login_token


class Details(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def details(self, ctx, username:str):
        """Get account details."""
        commander_id = ctx.author.id
        name_list = []
        all_data = list(token_base.find({"id": commander_id, "username": username}))
        for i in all_data:
            name_list.append(i['username'])
        if username in name_list:
            token = token_base.find_one({'username': username})['token']
            try:
                api = HQApi(token)
                data = api.get_users_me()
            except ApiResponseError:
                embed=discord.Embed(description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=0x00ffff)
                return await ctx.send(embed=embed)
            username = data["username"]
            id = data["userId"]
            avatar_url = data["avatarUrl"]
            upt = data["created"]
            uptm = aniso8601.parse_datetime(upt)
            uptim = uptm.astimezone(timezone("Asia/Kolkata"))
            created_at = uptim.strftime("%b %d, %Y %I:%M %p")
            ph_no = data["phoneNumber"]
            lives = data["items"]["lives"]
            superSpins = data["items"]["superSpins"]
            erasers = data["items"]["erase1s"]
            coins = data["coins"]
            api = HQApi(token)
            data = api.get_payouts_me()
            bal = data["balance"]
            total = bal["prizeTotal"]
            paid = bal["paid"]
            pending = bal["pending"]
            unpaid = bal["unpaid"]
            available = bal["available"]
            unclaimed = bal["frozen"]
            await ctx.send("Check your DM! Details send in DM's.")
            embed=discord.Embed(title=f"**__Statistics of HQ Account !__**", description=f"**Username: `{username}`\nMobile Number: `{ph_no}`**", color=0x00ff00)
            embed.add_field(name=f"**🔥 __Items(Lives, Spin, Erasers, Coins)__**", value=f"**• Total Coins : {coins}\n• Total Lives : {lives}\n• Super Spins : {superSpins}\n• Total Erasers : {erasers}**")
            embed.add_field(name="**💸 __Balance & Cashout Details :__-**", value=f"**• Total Balance : {total}\n• Claimed Ammount : {paid}\n• Pending Ammount : {pending}\n• Unclaimed Ammount : {unpaid}\n• Available for Cashout : {available}**")
            embed.set_footer(text=f"ID: {id} | Created At: {created_at}")
            embed.set_thumbnail(url=avatar_url)
            await ctx.author.send(embed=embed)
            
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=0x00ffff)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)

    
def setup(client):
    client.add_cog(Details(client))
