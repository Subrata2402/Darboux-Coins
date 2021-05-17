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


class Google(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["googlelink"])
    @commands.dm_only()
    async def glink(self, ctx):
        embed=discord.Embed(title="**HQ Google Login**", color=discord.Colour.random())
        embed.add_field(name="Login Link", value="[Click Here](https://accounts.google.com/o/oauth2/v2/auth?audience=668326540387-84isqp5u1s4dubes1tns5i7p2kgqefja.apps.googleusercontent.com&client_id=668326540387-isfa1c5ibd6h0mhm2h10n242q2uc131q.apps.googleusercontent.com&response_type=code&scope=email%20profile&&redirect_uri=https://localhost:8000&verifier=56778634)")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @glink.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, Exception):
            await ctx.send(f"{ctx.author.mention}, **You can use this command only in DM!**")


    @commands.command(aliases=["glinkverify","googleverify","hqglogin","hqgverify"])
    @commands.dm_only()
    async def gverify(self, ctx, url=None):
        if url is None:
            embed=discord.Embed(title="⚠️ Invalid Argument", description=f"Use `{ctx.prefix}gverify <url>` to add an HQ Trivia account in bot.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        embed=discord.Embed(title="Verification Disabled", description="Sorry, this process is not available right now. Please try again later.", color=discord.Colour.random())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/823971641959776326/834684689059020820/1200px-Google__G__Logo.svg.png")
        await ctx.send(embed=embed)

    @gverify.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, Exception):
            await ctx.send(f"{ctx.author.mention}, **You can use this command only in DM!**")



def setup(client):
    client.add_cog(Google(client))
