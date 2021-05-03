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


class Show(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def show(self, ctx):
        """Get HQ Next all Shows Details."""
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjI3MTk2MTg0LCJ1c2VybmFtZSI6IkVsb3Vpc2U0MiIsImF2YXRhclVybCI6Imh0dHBzOi8vY2RuLnByb2QuaHlwZS5zcGFjZS9kYS9nb2xkLnBuZyIsInRva2VuIjoiYU5zZjQyIiwicm9sZXMiOltdLCJjbGllbnQiOiJBbmRyb2lkLzEuNDkuOCIsImd1ZXN0SWQiOm51bGwsInYiOjEsImlhdCI6MTYxNjkyMDUxNiwiZXhwIjoxNjI0Njk2NTE2LCJpc3MiOiJoeXBlcXVpei8xIn0.LNyUoO_iD7FBY0H4NUaD_rkHCrQCvbugAoIqHc5Lwr0"
        api = HQApi(token)
        data = api.get_schedule()
        description_info = f""
        for data in data["shows"]:
            name = data["display"]["title"]
            tim = data["startTime"]
            tm = aniso8601.parse_datetime(tim)
            x_ind = tm.astimezone(timezone("Asia/Kolkata"))
            time = x_ind.strftime("%d-%m-%Y %I:%M %p")
            prize = data["prizeCents"]
            prize = int(prize)/int(100)
            prize = '{:,}'.format(int(prize))
            description_info += f"**• Show Name : {name}\n• Show Time : {time}\n• Prize Money : ${prize}**\n\n"
        embed=discord.Embed(title="**__HQ Next Show Details !__**", description=description_info, color=0x00ff00)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def nextshow(self, ctx):
        """Get HQ next show details."""
        api = HQApi()
        response_data = api.get_show()
        tim = (response_data["nextShowTime"])
        tm = aniso8601.parse_datetime(tim)
        x_ind = tm.astimezone(timezone("Asia/Kolkata"))
        time = x_ind.strftime("%d-%m-%Y %I:%M %p")
        prize = (response_data["nextShowPrize"])
        for data in response_data["upcoming"]:
            type = data["nextShowLabel"]["title"]
        embed=discord.Embed(title="**__HQ Next Show Details !__**", description=f"**• Show Name : {type}\n• Show Time : {time}\n• Prize Money : {prize}**", color=0x00FBFF)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/799237115962851348/816261537101905951/1200px-HQ_logo.svg.png")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Show(client))
