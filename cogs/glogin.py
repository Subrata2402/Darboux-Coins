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
import urllib
from urllib.parse import unquote


class Google(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def get_id_token(self, url):
        access_token = url.split("?code=")[1].split("&scope")[0]
        url = 'https://www.googleapis.com/oauth2/v4/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        code = unquote(access_token)
        data = {"audience":'668326540387-84isqp5u1s4dubes1tns5i7p2kgqefja.apps.googleusercontent.com',
                   "client_id":'668326540387-isfa1c5ibd6h0mhm2h10n242q2uc131q.apps.googleusercontent.com',#'668326540387-isfa1c5ibd6h0mhm2h10n242q2uc131q.apps.googleusercontent.com',
                   "code": code,#"4%2F0AY0e-g7T6nfb3XAPZueeZA3lOo9m03ysOn7pnlbuQsgIgyA86QWzt4bkz1zh94a4J0ZwKQ",#"4%2F0AY0e-g51-ROwgrpCSsZDe8dyIeCT--MmUpbUUFZ2hGpIkMMK0U_76LmzzOeiZJHjvZeH9A",
                   "grant_type":"authorization_code",
                   "redirect_uri":"http://localhost:8080",#"com.googleusercontent.apps.668326540387-isfa1c5ibd6h0mhm2h10n242q2uc131q:/oauth2callback",
                   "verifier":'56778634'}#72103384}
        response = requests.post(url = url, headers = headers, data = data).json()
        id_token = response.get("id_token")
        return id_token
        

    @commands.command(aliases=["googlelink"])
    @commands.dm_only()
    async def glink(self, ctx):
        if ctx.guild:
            try:
                await ctx.message.delete()
            except:
                pass
            await ctx.send(f"{ctx.author.mention}, **Check your DM!**")
        embed=discord.Embed(title="**HQ Google Login**", description=f"**[Click Here](https://accounts.google.com/o/oauth2/v2/auth?audience=668326540387-84isqp5u1s4dubes1tns5i7p2kgqefja.apps.googleusercontent.com&client_id=668326540387-isfa1c5ibd6h0mhm2h10n242q2uc131q.apps.googleusercontent.com&response_type=code&scope=email%20profile&&redirect_uri=http://localhost:8080&verifier=56778634) to login HQ Trivia with Google Account.\n\nUse `{ctx.prefix}gmethod` to get all process of Google Login.**", color=discord.Colour.random())
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
        id_token = await self.get_id_token(url)
        api = HQApi()
        if not id_token:
            return await ctx.send(ctx.author.mention + ", **Invalid URL provided!**")
        data = api.google_login(id_token)
        id = data["userId"]
        username = data["username"]
        login_token = data["loginToken"]
        access_token = data["accessToken"]
        check_if_exist = token_base.find_one({"id": user_id,
                                              "user_id": id})
        if check_if_exist == None:
            user_info_dict = {'id': user_id,
                              'token': access_token,
                              'username': username, 'user_id': id}
            token_base.insert_one(user_info_dict)
            user_info_dict = {'id': user_id,
                              'login_token': login_token,
                              'access_token': access_token,
                              'username': username, 'user_id': id}
            login_token_base.insert_one(user_info_dict)
            embed=discord.Embed(title="Account Added ✅", description=f"Successfully add an account with name `{username}`", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)
            await channel.send(f"{ctx.author} add a account via Facebook.")
        else:
            embed=discord.Embed(title="⚠️ Already Exists", description="This account already exists in bot database. You can't add it again.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)



def setup(client):
    client.add_cog(Google(client))
