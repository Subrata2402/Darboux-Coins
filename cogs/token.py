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
        token = token_base.find_one({'username': username})['token']
        api = HQApi(token)
        data = api.get_login_token()
        lt = data["loginToken"]
        data = api.get_tokens(lt)
        username = data["username"]
        login_token = data["loginToken"]
        access_token = data["accessToken"]
        await ctx.send(f"```\n{access_token}\n```")

    
    @commands.command(pass_context=True, aliases=['addt'])
    @commands.dm_only()
    async def addtoken(self, ctx, token=None):
        """Add token in bot database."""
        if token is None:
            embed=discord.Embed(title="⚠️ Invalid Argument", description=f"You didn't put token after `{ctx.prefix}addtoken`. Please use correct : `{ctx.prefix}addtoken [token]`", color=0x00ffff)
            return await ctx.send(embed=embed)
        channel = self.client.get_channel(841489971109560321)
        try:
            api = HQApi(token)
            data = api.get_users_me()
            username = data["username"]
            id = data["userId"]
            user_id = ctx.author.id
            data = api.get_login_token()
            lt = data["loginToken"]
        except ApiResponseError:
            embed=discord.Embed(title="⚠️ Api Response Error", description="This is not a valid token or token is expired. Try again with a valid token or which is not expire!", color=0x00ff00)
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
            embed=discord.Embed(title="Account Added ✅", description=f"Successfully add an account with name `{username}`", color=0x00ffff)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)
            await channel.send(f"{ctx.author} add a account via access token.")
        else:
            embed=discord.Embed(title="⚠️ Already Exists", description="This account already exists in bot database. You can't add it again.", color=0x00ff00)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)

    @addtoken.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send(f"{ctx.author.mention}, **You can add token with bot only in DM's.**")
            await ctx.author.send(f"{ctx.author.mention}, **You can add token here.**")

    @commands.command(pass_context=True)
    async def token(self, ctx, username=None):
        """Get save access token."""
        if username is None:
            embed=discord.Embed(title="⚠️ Invalid Argument", description=f"You didn't put username after `{ctx.prefix}token`. Please use correct : `{ctx.prefix}token [username]`", color=0x00ffff)
            return await ctx.send(embed=embed)
        commander_id = ctx.author.id
        name_list = []
        all_data = list(token_base.find({"id": commander_id, "username": username}))
        for i in all_data:
            name_list.append(i['username'])
        if username in name_list:
            spec_user_token = token_base.find_one({'username': username})['token']
            await ctx.send(f"{ctx.author.mention}, Check your DM!")
            embed=discord.Embed(title=f"{username} | Access Token", description=f"`{spec_user_token}`", color=0x00ffff)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.author.send(embed=embed)
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `+accounts` to check your all accounts.", color=0x00ffff)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)
    
    @token.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, Exception):
            await ctx.send(f'```\n{error}\n```')

    @commands.command()
    async def accounts(self, ctx):
        commander_id = ctx.author.id
        id_list = []
        all_data = list(token_base.find({"id": commander_id}))
        for i in all_data:
            id_list.append(i['id'])
        if commander_id not in id_list:
            embed=discord.Embed(title="❎ Not Found", description=f"You have not added any accounts. Use Command `+add +(country code)(number)` or `+addtoken (token)` to save your account in bot database and make unlimited coins with bot.", color=0x00ffff)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        name_list = []
        all_data = list(token_base.find({"id": commander_id}))
        name = f""
        s = 0
        for i in all_data:
            name_list.append(i['username'])
        for username in name_list:
            s = int(s) + 1
            name += f"{s} - {username}\n"
        embed=discord.Embed(title=f"{ctx.author.name}'s accounts !", description=name, color=0x00ffff)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    

def setup(client):
    client.add_cog(Token(client))
