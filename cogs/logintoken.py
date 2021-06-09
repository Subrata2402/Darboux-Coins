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


class LoginToken(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def getlt(self, ctx, username:str):
        """Get login token."""
        token = token_base.find_one({'username': username})['token']
        api = HQApi(token)
        data = api.get_login_token()
        lt = data["loginToken"]
        await ctx.send(f"```\n{lt}\n```")

    @commands.command()
    @commands.is_owner()
    async def addlt(self, ctx, username:str):
        """Add login token in bot database."""
        token = token_base.find_one({'username': username})['token']
        api = HQApi(token)
        data = api.get_login_token()
        lt = data["loginToken"]
        data = api.get_tokens(lt)
        username = data["username"]
        id = data["userId"]
        login_token = data["loginToken"]
        access_token = data["accessToken"]
        user_id = ctx.author.id
        check_if_exist = login_token_base.find_one({"id": user_id,
                                                    "login_token": login_token})
        if check_if_exist == None:
            user_info_dict = {'id': user_id,
                              'login_token': login_token,
                              'access_token': access_token,
                              'username': username, "user_id": id}
            login_token_base.insert_one(user_info_dict)
            await ctx.send(f"**Successfully add this account with name ||{username}||**")
        else:
            await ctx.send(f"**This account already linked with bot.**")


    @commands.command()
    @commands.is_owner()
    async def update(self, ctx):
        token_list = []
        all_data = list(token_base.find({"id": ctx.author.id}))
        for i in all_data:
            token_list.append(i['token'])
        for token in token_list:
            api = HQApi(token)
            data = api.get_users_me()
            id = data["userId"]
            update = {"user_id": id}
            token_base.update_one({"token": token}, {"$set": update})
        await ctx.send("success")


def setup(client):
    client.add_cog(LoginToken(client))
