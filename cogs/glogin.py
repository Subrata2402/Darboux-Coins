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



class Google(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["googlelink"])
    @commands.dm_only()
    async def glink(self, ctx):
        if ctx.guild:
            try:
                await ctx.message.delete()
            except:
                pass
            await ctx.send(f"{ctx.author.mention}, **Check your DM!**")
        embed=discord.Embed(title="**HQ Google Login**", description=f"**[Click Here](https://accounts.google.com/o/oauth2/v2/auth?audience=668326540387-84isqp5u1s4dubes1tns5i7p2kgqefja.apps.googleusercontent.com&client_id=668326540387-isfa1c5ibd6h0mhm2h10n242q2uc131q.apps.googleusercontent.com&response_type=code&scope=email%20profile&&redirect_uri=https://localhost:8000&verifier=56778634) to login HQ Trivia with Google Account.\n\nUse `{ctx.prefix}gmethod` to get all process of Google Login.**", color=discord.Colour.random())
        #embed.add_field(name="Login Link", value="[Click Here](87-isfa1c5ibd6h0mhm2h10n242q2uc131q.apps.googleusercontent.com&response_type=code&scope=email%20profile&&redirect_uri=https://localhost:8000&verifier=56778634)")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.author.send(embed=embed)


    @commands.command(aliases=["glinkverify","googleverify","glogin","hqgverify"])
    @commands.dm_only()
    async def gverify(self, ctx, url=None):
        if ctx.guild:
            try:
                await ctx.message.delete()
            except:
                pass
            return await ctx.send(f"{ctx.author.mention}, **You can use this command only in DM!**")
        if url is None:
            embed=discord.Embed(title="⚠️ Invalid Argument", description=f"Use `{ctx.prefix}glogin <url>` to add an HQ Trivia account in bot.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        embed=discord.Embed(title="⚠️ Google Login", description="Sorry, this process is temporary not available. Please try again later.", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)



def setup(client):
    client.add_cog(Google(client))
