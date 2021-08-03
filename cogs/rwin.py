import discord
import random
from discord.ext import commands
import asyncio
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
from database.db import token_base, login_token_base



class RecentWins(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def rwins(self, ctx, username:str):
        """Check recent winnings by spamming."""
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
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            username = data["username"]
            api = HQApi(token)
            data = api.get_payouts_me()
            for rwin in data["recentWins"]:
                prize = rwin["prize"]
                windate = rwin["winDate"]
                tm = aniso8601.parse_datetime(windate)
                x =  tm.strftime("%H:%M:%S [%d/%m/%Y] ")
                x_ind = tm.astimezone(timezone("Asia/Kolkata"))
                x_time = x_ind.strftime("%b %d, %Y %I:%M %p")
                embed=discord.Embed(title=f"**__{username}'s Winnings Info !__**", description=f"**• Prize Money: {prize}\n• Winning Date: {x_time}**", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)

    @rwins.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, Exception):
            await ctx.send(f'```\n{error}\n```')

    @commands.command()
    async def recentwins(self, ctx, username:str):
        """Get recent winnings."""
        commander_id = ctx.author.id
        name_list = []
        all_data = list(token_base.find({"id": commander_id, "username": username}))
        for i in all_data:
            name_list.append(i['username'])
        if username in name_list:
            token = token_base.find_one({'username': username})['token']
            try:
                api = HQApi(token)
            except ApiResponseError:
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            data = api.get_users_me()
            username = data["username"]
            api = HQApi(token)
            data = api.get_payouts_me()
            description_info=f""
            s = 0
            for rwin in data["recentWins"]:
                s = int(s) + 1
                if s > 30:
                    break
                prize = rwin["prize"]
                windate = rwin["winDate"]
                tm = aniso8601.parse_datetime(windate)
                x =  tm.strftime("%H:%M:%S [%d/%m/%Y] ")
                x_ind = tm.astimezone(timezone("Asia/Kolkata"))
                x_time = x_ind.strftime("%d-%m-%Y")
                description_info += f"**{s}. {x_time} : {prize}**\n"
            embed=discord.Embed(title=f"**__{username}'s Winnings Info !__**", description=description_info, color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)

    @recentwins.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, Exception):
            await ctx.send(f'```\n{error}\n```')

def setup(client):
    client.add_cog(RecentWins(client))
