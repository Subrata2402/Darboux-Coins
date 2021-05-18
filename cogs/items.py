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
    async def life(self, ctx, amount=None, username=None):
        """Purchase Life."""
        if not amount or not username:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}cashout [email] [username]` to cashout from your HQ Trivia account.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        commander_id = ctx.author.id
        name_list = []
        all_data = list(token_base.find({"id": commander_id, "username": username}))
        for i in all_data:
            name_list.append(i['username'])
        if username not in name_list:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        token = token_base.find_one({'username': username})['token']
        try:
            api = HQApi(token)
            data = api.get_users_me()
        except ApiResponseError:
            embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        headers = {"Authorization": f"Bearer {token}"}
        try:
            amount = int(amount)
        except:
            await ctx.send(f"{amount} is not a valid amount.")
        if amount == int(1):
            r = requests.post("https://api-quiz.hype.space/store/com.intermedia.hq.item.extralife.1x/purchase", headers=headers)
        elif amount == int(3):
            r = requests.post("https://api-quiz.hype.space/store/com.intermedia.hq.item.extralife.3x/purchase", headers=headers)
        elif amount == int(5):
            r = requests.post("https://api-quiz.hype.space/store/com.intermedia.hq.item.extralife.5x/purchase", headers=headers)
        else:
            embed=discord.Embed(title="⚠️ Api Response Error", description=f"You can't purchase {amount} life(s). Please choose an amount between 1, 3 and 5.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        data = r.json()



def setup(client):
    client.add_cog(Details(client))
