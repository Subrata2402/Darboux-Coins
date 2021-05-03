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
    async def fblink(self, ctx):
        embed=discord.Embed(title="**HQ Facebook Login Link**", description="**Login Link : [Click Here](https://m.facebook.com/v9.0/dialog/oauth?auth_type=rerequest&cbt=1613638985174&client_id=1309867799121574&default_audience=friends&display=touch&e2e=%7B%22init%22%3A1596063.1199975831%7D&fbapp_pres=1&ies=0&nonce=EC40E5E9-148C-4D27-955B-54A3B8635F47&redirect_uri=fb1309867799121574%3A%2F%2Fauthorize%2F&response_type=id_token%2Ctoken_or_nonce%2Csigned_request%2Cgraph_domain&return_scopes=true&scope=email%2Copenid&sdk=ios&sdk_version=9.0.0&state=%7B%22challenge%22%3A%22weDSTppN3JYneIZMp63Vd71MOZ0%253D%22%2C%220_auth_logger_id%22%3A%22361441EC-F569-418B-9E84-E0703A60B519%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D)**", color=0x00ffff)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/775384878942257173/834676722145165352/facebook-512.png")
        await ctx.send(embed=embed)

    @commands.command(aliases=["fblogin"])
    async def fbverify(self, ctx, url):
        embed=discord.Embed(title="Verification Disabled", description="Sorry, this process is not available right now. Please try again later.", color=0x00ffff)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/775384878942257173/834676722145165352/facebook-512.png")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(FacebookLogin(client))
