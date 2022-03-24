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



class Refresh(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Refresh"])
    async def refresh(self, ctx, username=None):
        """Refresh an account.."""
        if username is None:
            embed=discord.Embed(title="⚠️ Invalid Argument", description=f"You didn't put username after `{ctx.prefix}refresh`. Please use correct : `{ctx.prefix}refresh [username]`", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        embed=discord.Embed(title="Refreshing...", color=discord.Colour.random())
        x = await ctx.send(embed=embed)
        commander_id = ctx.author.id
        check_id = login_token_base.find_one({"id": commander_id, "username": username})
        if not check_id:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await x.edit(embed=embed)
        try:
            api = HQApi()
            token = login_token_base.find_one({'username': username})['login_token']
            data = api.get_tokens(token)
            name = data["username"]
            access_token = data["accessToken"]
            update = ({'token': access_token})
            token_base.update_one({'username': username}, {'$set': update})
            update = ({'username': name})
            token_base.update_one({'username': username}, {'$set': update})
            login_token_base.update_one({'username': username}, {'$set': update})
            embed=discord.Embed(title="Successfully refreshed your account ✅", color=discord.Colour.random())
            await x.edit(embed=embed)
        except Exception as e:
            print(e)
            embed=discord.Embed(title="Refreshing Failed!", color=discord.Colour.random())
            await x.edit(embed=embed)


def setup(client):
    client.add_cog(Refresh(client))
