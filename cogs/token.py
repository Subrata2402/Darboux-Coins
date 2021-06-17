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


class Token(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def getact(self, ctx, username:str):
        """Get random access token."""
        token = login_token_base.find_one({'username': username})['login_token']
        api = HQApi()
        data = api.get_tokens(token)
        username = data["username"]
        login_token = data["loginToken"]
        access_token = data["accessToken"]
        await ctx.send(f"```\n{access_token}\n```")

    
    @commands.command(pass_context=True, aliases=['addt'])
    async def addtoken(self, ctx, token=None):
        """Add token in bot database."""
        if token is None:
            embed=discord.Embed(title="⚠️ Invalid Argument", description=f"You didn't put token after `{ctx.prefix}addtoken`. Please use correct : `{ctx.prefix}addtoken [token]`", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        channel = self.client.get_channel(841489971109560321)
        if ctx.guild:
            return await ctx.send(f"{ctx.author.mention}, **You can add token with bot only in DM's.**")
        try:
            api = HQApi(token)
            data = api.get_users_me()
            username = data["username"]
            id = data["userId"]
            user_id = ctx.author.id
            data = api.get_login_token()
            lt = data["loginToken"]
        except ApiResponseError:
            embed=discord.Embed(title="⚠️ Api Response Error", description="This is not a valid token or token is expired. Try again with a valid token or which is not expire!", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        check_if_exist = token_base.find_one({"id": user_id,
                                              "user_id": id})
        if check_if_exist == None:
            user_info_dict = {'id': user_id,
                              'token': token,
                              'username': username, 'user_id': id}
            token_base.insert_one(user_info_dict)
            user_info_dict = {'id': user_id,
                              'login_token': lt,
                              'access_token': token,
                              'username': username, 'user_id': id}
            login_token_base.insert_one(user_info_dict)
            embed=discord.Embed(title="Account Added ✅", description=f"Successfully add an account with name `{username}` in bot database.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)
            await channel.send(f"{ctx.author} add a account via access token.")
        else:
            embed=discord.Embed(title="⚠️ Already Exists", description=f"This account already exists in bot database with name `{username}`. You can't add it again.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    async def token(self, ctx, username=None):
        """Get save access token."""
        if username is None:
            embed=discord.Embed(title="⚠️ Invalid Argument", description=f"You didn't put username after `{ctx.prefix}token`. Please use correct : `{ctx.prefix}token [username]`", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        commander_id = ctx.author.id
        name_list = []
        all_data = list(token_base.find({"id": commander_id, "username": username}))
        for i in all_data:
            name_list.append(i['username'])
        if ctx.guild:
            await ctx.send(f"{ctx.author.mention}, Check your DM!")
        if username in name_list:
            spec_user_token = token_base.find_one({'username': username})['token']
            embed=discord.Embed(title=f"{username} | Access Token", description=f"`{spec_user_token}`", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.author.send(embed=embed)
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Token(client))
