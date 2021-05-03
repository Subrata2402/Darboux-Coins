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


class Friends(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def friends(self, ctx, username=None):
        """Get friend lists."""
        if username is None:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}friends [username]` to check your all friends list.", color=0x00ffff)
            return await ctx.send(embed=embed)
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
        token = token_base.find_one({'username': username})['token']
        try:
            api = HQApi(token)
            data = api.get_users_me()
        except ApiResponseError:
            embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=0x00ffff)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        username = data["username"]
        url = "https://api-quiz.hype.space/friends"
        headers = {"Authorization": f"Bearer {token}",
                   "x-hq-client": "Android/1.3.0"}
        r = requests.get(url = url, headers=headers).json()
        description_info = f""
        for data in r["data"]:
            name = data["username"]
            total = data["leaderboard"]["total"]
            highScore = data["highScore"]
            gamesPlayed = data["gamesPlayed"]
            winCount = data["winCount"]
            description_info += f"• Username: **{name}** ({total})\n• Description: **({gamesPlayed}, {winCount}, {highScore})**\n\n"
        embed=discord.Embed(title=f"**__{username}'s Friends List !__**", description=description_info, color=0x00ff00)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def addfriend(self, ctx, username=None, name=None):
        """Send friend request."""
        if not username or not name:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}addfriend [username] [friend's username]` to send a friend request.", color=0x00ffff)
            return await ctx.send(embed=embed)
        commander_id = ctx.author.id
        name_list = []
        all_data = list(token_base.find({"id": commander_id, "username": username}))
        for i in all_data:
            name_list.append(i['username'])
        if username in name_list:
            token = token_base.find_one({'username': username})['token']
            try:
                api = HQApi(token)
                data = api.search(name)
                id = data["data"][0]["userId"]
            except ApiResponseError:
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=0x00ffff)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            try:
                data = api.add_friend(id)
                embed=discord.Embed(title="**Request Send Done ✅**", description=f"**Successfully sent friend request to `{name}`**", color=0x00ff00)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
            except:
                embed=discord.Embed(title="**Request Send Failed ⚠️**", description=f"**Couldn't sent Friend Request to `{name}`.**", color=0x00ff00)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=0x00ffff)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)

    @addfriend.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, Exception):
            await ctx.send(f'```\n{error}\n```')

    @commands.command()
    async def acceptfriend(self, ctx, username=None, name=None):
        """Accept friend request."""
        if not username or not name:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}acceptfriend [username] [friend's username]` to accept a friend request.", color=0x00ffff)
            return await ctx.send(embed=embed)
        commander_id = ctx.author.id
        name_list = []
        all_data = list(token_base.find({"id": commander_id, "username": username}))
        for i in all_data:
            name_list.append(i['username'])
        if username in name_list:
            token = token_base.find_one({'username': username})['token']
            try:
                api = HQApi(token)
                data = api.search(name)
                id = data["data"][0]["userId"]
            except ApiResponseError:
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=0x00ffff)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            try:
                data = api.accept_friend(id)
                embed=discord.Embed(title="**Friend Request Accepted ✅**", description=f"**Successfully accept friend request `{name}`**", color=0x00ff00)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
            except:
                embed=discord.Embed(title="**Failed to Request Accept ⚠️**", description=f"**Couldn't find user `{name}`.**", color=0x00ff00)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=0x00ffff)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)

    @acceptfriend.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, Exception):
            await ctx.send(f'```\n{error}\n```')

    @commands.command()
    async def removefriend(self, ctx, username=None, name=None):
        """Remove a Friend from your friends list."""
        if not username or not name:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}removefriend [username] [friend's username]` to remove a friend from your friends list.", color=0x00ffff)
            return await ctx.send(embed=embed)
        commander_id = ctx.author.id
        name_list = []
        all_data = list(token_base.find({"id": commander_id, "username": username}))
        for i in all_data:
            name_list.append(i['username'])
        if username in name_list:
            token = token_base.find_one({'username': username})['token']
            try:
                api = HQApi(token)
                data = api.search(name)
                id = data["data"][0]["userId"]
            except ApiResponseError:
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=0x00ffff)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            try:
                data = api.remove_friend(id)
                embed=discord.Embed(title="**Friend Removed ✅**", description=f"**Successfully friend removed `{name}`**", color=0x00ff00)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
            except:
                embed=discord.Embed(title="**Failed to Remove Friend ⚠️**", description=f"**Couldn't find user `{name}`.**", color=0x00ff00)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=0x00ffff)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)

    @removefriend.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, Exception):
            await ctx.send(f'```\n{error}\n```')

    @commands.command()
    async def friendstatus(self, ctx, username=None, name=None):
        """Get friends stats."""
        if not username or not name:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}friendstatus [username] [Friend's username]` to check your friend's status.", color=0x00ffff)
            return await ctx.send(embed=embed)
        commander_id = ctx.author.id
        name_list = []
        all_data = list(token_base.find({"id": commander_id, "username": username}))
        for i in all_data:
            name_list.append(i['username'])
        if username in name_list:
            token = token_base.find_one({'username': username})['token']
            try:
                api = HQApi(token)
                data = api.search(name)
                id = data["data"][0]["userId"]
            except ApiResponseError:
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=0x00ffff)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            data = api.friend_status(id)
            embed=discord.Embed(title="Friend Status", description=f"**Status : {data['status']}**", color=0x00ff00)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=0x00ffff)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)

    @friendstatus.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, Exception):
            await ctx.send(f'```\n{error}\n```')

def setup(client):
    client.add_cog(Friends(client))
