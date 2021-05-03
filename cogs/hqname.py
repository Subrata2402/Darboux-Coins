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


class HQName(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hqname(self, ctx):
        """Get HQ Random US Name."""
        embed=discord.Embed(title="Random US Name Generator", color=0x00ffff)
        embed.add_field(name="Name:", value="Generating...")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=embed)
        r = requests.get("https://api.namefake.com")
        res = r.json()
        name = res["name"]
        embed=discord.Embed(title="Random US Name Generator", color=0x00ffff)
        embed.add_field(name="Name:", value=name)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        await msg.edit(embed=embed)

def setup(client):
    client.add_cog(HQName(client))
