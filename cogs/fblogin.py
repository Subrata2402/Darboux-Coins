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


class FacebookLogin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["flink"])
    @commands.dm_only()
    async def fblink(self, ctx):
        embed=discord.Embed(title="**HQ Facebook Login**", color=discord.Colour.random())
        embed.add_field(name="Login Link", value="[Click Here](https://m.facebook.com/v9.0/dialog/oauth?auth_type=rerequest&cbt=1613638985174&client_id=1309867799121574&default_audience=friends&display=touch&e2e=%7B%22init%22%3A1596063.1199975831%7D&fbapp_pres=1&ies=0&nonce=EC40E5E9-148C-4D27-955B-54A3B8635F47&redirect_uri=fb1309867799121574%3A%2F%2Fauthorize%2F&response_type=id_token%2Ctoken_or_nonce%2Csigned_request%2Cgraph_domain&return_scopes=true&scope=email%2Copenid&sdk=ios&sdk_version=9.0.0&state=%7B%22challenge%22%3A%22weDSTppN3JYneIZMp63Vd71MOZ0%253D%22%2C%220_auth_logger_id%22%3A%22361441EC-F569-418B-9E84-E0703A60B519%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D)")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @fblink.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, Exception):
            await ctx.send(f"{ctx.author.mention}, **You can use this command only in DM!**")

    @commands.command(aliases=["fblogin", "hqflogin", "hqfblogin"])
    @commands.dm_only()
    async def fbverify(self, ctx, token=None):
        channel = self.client.get_channel(841489971109560321)
        user_id = ctx.author.id
        if token is None:
            embed=discord.Embed(title="⚠️ Invalid Argument", description=f"Use `{ctx.prefix}fblogin <fbtoken>` to add your HQ Trivia account in bot database.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        api = HQApi()
        #data = requests.post(url="https://api-quiz.hype.space/users/provider-auth", data={"type":"FACEBOOK","token": token}).json()
        r = api.facebook_login(token)
        data = r.json()
        print(data)
        try:
            api = HQApi()
            #data = requests.post(url="https://api-quiz.hype.space/users/provider-auth", data={"type":"FACEBOOK","token": token}).json()
            r = api.facebook_login(token)
            data = r.json()
            id = data["userId"]
            username = data["username"]
            login_token = data["loginToken"]
            access_token = data["accessToken"]
        except:
            embed=discord.Embed(title="⚠️ Api Response Error", description="This is not a valid token or token is expired. Try again with a valid token or which is not expire!", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
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
        

    @fbverify.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, Exception):
            await ctx.send(f"{ctx.author.mention}, **You can use this command only in DM!**")

def setup(client):
    client.add_cog(FacebookLogin(client))
