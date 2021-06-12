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


class UserStats(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["user", "hqstats", "hqstat"])
    async def hquser(self, ctx, name:str):
        """Get any user's stats."""
        token = token_base.find_one({"username": "bernita48"})["token"]
        api = HQApi(token)
        data = api.get_users_me()
        try:
            data = api.search(name)
            id = data["data"][0]["userId"]
            data = api.get_user(id)
            print(data)
            username = data["username"]
            id = data["userId"]
            avatar_url = data["avatarUrl"]
            create_at = data["created"]
            tm = aniso8601.parse_datetime(create_at)
            x =  tm.strftime("%H:%M:%S [%d/%m/%Y] ")
            x_ind = tm.astimezone(timezone("Asia/Kolkata"))
            at = x_ind.strftime("%d-%m-%Y %I:%M %p")
            total = data["leaderboard"]["total"]
            unclaimed = data["leaderboard"]["unclaimed"]
            winCount = data["winCount"]
            gamesPlayed = data["gamesPlayed"]
            highScore = data["highScore"]
            embed=discord.Embed(title=f"**__{username}'s account details !__**", description=f"**• Username : {username}\n• Total Winnings : {total}\n• Unclaimed : {unclaimed}\n• Total Games Played : {gamesPlayed}\n• Total Wins : {winCount}\n• High Score : {highScore}**", color=discord.Colour.random())
            embed.set_thumbnail(url=avatar_url)
            embed.set_footer(text=f"User ID : {id} | Created At : {at}")
            await ctx.send(embed=embed)
        except:
            embed=discord.Embed(title="❎ Not Found", description=f"Couldn't find any HQ account account with name `{name}`.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(UserStats(client))
