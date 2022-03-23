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



class Swipe(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def swipe(self, ctx, username=None):
        """Swipe and earn extra life."""
        if username is None:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}swipe [username]` to swipe your account and earn an Extra Life.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        commander_id = ctx.author.id
        check_id = token_base.find_one({"id": commander_id, "username": username})
        if not check_id:
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
        embed=discord.Embed(title=f"Swiping...", color=discord.Colour.random())
        x = await ctx.send(embed=embed)
        await asyncio.sleep(2)
        try:
            r = api.swipe()
            data = r["data"]
            embed=discord.Embed(title="Swiped Done ✅", description=f"You have successfully swiped your account and earn an Extra <:extra_life:844448511264948225> Life.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await x.edit(embed=embed)
        except:
            embed=discord.Embed(title="⚠️ Swiped Failed", description=f"You have already swiped your account in this month.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await x.edit(embed=embed)


def setup(client):
    client.add_cog(Swipe(client))
