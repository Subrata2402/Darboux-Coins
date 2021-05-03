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


class Refresh(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def refresh(self, ctx, username:str):
        """Refresh an account.."""
        x = await ctx.send("**Refreshing...**")
        commander_id = ctx.author.id
        name_list = []
        all_data = list(token_base.find({"id": commander_id, "username": username}))
        for i in all_data:
            name_list.append(i['username'])
        if username not in name_list:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=0x00ffff)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        try:
            token = login_token_base.find_one({'username': username})['access_token']
            api = HQApi(token)
            data = api.get_login_token()
            lt = data["loginToken"]
            data = api.get_tokens(lt)
            print(data)
            name = data["username"]
            access_token = data["accessToken"]
            update = ({'token': access_token})
            token_base.update_one({'username': username}, {'$set': update})
            update = ({'username': name})
            token_base.update_one({'username': username}, {'$set': update})
            login_token_base.update_one({'username': username}, {'$set': update})
            await x.edit(content="**Successfully refreshed your account ✅**")
        except:
            await x.edit(content="**Refreshing Failed!**")

    @refresh.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, Exception):
            await ctx.send(f'```\n{error}\n```')



def setup(client):
    client.add_cog(Refresh(client))
