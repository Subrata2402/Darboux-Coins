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


class Details(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["bal"])
    async def balance(self, ctx):
        """Get account details."""
        commander_id = ctx.author.id
        name_list = []
        id_list = []
        all_data = list(token_base.find({"id": commander_id}))
        for i in all_data:
            name_list.append(i['username'])
        for j in all_data:
            id_list.append(j['id'])
        if commander_id not in id_list:
            embed=discord.Embed(title="❎ Not Found", description=f"You have not added any accounts. Use Command `{ctx.prefix}add +(country code)(number)` or `{ctx.prefix}addtoken (token)` or `{ctx.prefix}fblogin (fbtoken)` to save your account in bot database and make unlimited coins with bot.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        embed=discord.Embed(title="Fetching your account balance and Cashout details...", color=0x00ffff)
        x = await ctx.send(embed=embed)
        description = ""
        total = 0
        paid = 0
        pending = 0
        unpaid = 0
        available = 0
        for username in name_list:
            token = token_base.find_one({'username': username})['token']
            api = HQApi(token)
            data = api.get_payouts_me()
            total = float(total) + float(bal["prizeTotal"][1:])
            paid = float(paid) + float(bal["paid"][1:])
            pending = float(pending) + float(bal["pending"][1:])
            unpaid = float(unpaid) + float(bal["unpaid"][1:])
            available = float(available) + float(bal["available"][1:])
            total = "{:.2f}".format(total)
            paid = "{:.2f}".format(paid)
            pending = "{:.2f}".format(pending)
            unpaid = "{:.2f}".format(unpaid)
            available = "{:.2f}".format(available)
            embed=discord.Embed(title="Balance & Cashout Details of all Accounts", description=f"**• Total Balance :** ${total}\n**• Claimed Ammount :** ${paid}\n**• Pending Ammount :** ${pending}\n**• Unclaimed Ammount :** ${unpaid}\n**• Available for Cashout :** ${available}", color=discord.Colour.random())
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/844442503976583178.gif")
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await x.edit(embed=embed)
            
        embed=discord.Embed(title="Balance & Cashout Details of all Accounts", description=f"**• Total Balance :** ${total}\n**• Claimed Ammount :** ${paid}\n**• Pending Ammount :** ${pending}\n**• Unclaimed Ammount :** ${unpaid}\n**• Available for Cashout :** ${available}", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await x.edit(embed=embed)

def setup(client):
    client.add_cog(Details(client))
