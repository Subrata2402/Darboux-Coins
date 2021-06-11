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


class Profile(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def accounts(self, ctx):
        commander_id = ctx.author.id
        id_list = []
        all_data = list(token_base.find({"id": commander_id}))
        for i in all_data:
            id_list.append(i['id'])
        if commander_id not in id_list:
            embed=discord.Embed(title="❎ Not Found", description=f"You have not linked any of your accounts in the bot database.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        name_list = []
        all_data = list(token_base.find({"id": commander_id}))
        name = f""
        s = 0
        for i in all_data:
            name_list.append(i['username'])
        for username in name_list:
            s = int(s) + 1
            name += f"{s} - {username}\n"
        embed=discord.Embed(title=f"{ctx.author.name}'s accounts !", description=name, color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def profile(self, ctx):
        commander_id = ctx.author.id
        id_list = []
        all_data = list(token_base.find({"id": commander_id}))
        for i in all_data:
            id_list.append(i['id'])
        if commander_id not in id_list:
            embed=discord.Embed(title="❎ Not Found", description=f"You have not added any accounts. Use Command `{ctx.prefix}add +(country code)(number)` or `{ctx.prefix}addtoken (token)` or `{ctx.prefix}fblogin (fbtoken)` to save your account in bot database and make unlimited coins with bot.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        embed=discord.Embed(title="**Loading A/c(s)...**", color=discord.Colour.random())
        x = await ctx.send(embed=embed)
        token_list = []
        all_data = list(token_base.find({"id": commander_id}))
        for i in all_data:
            token_list.append(i['token'])
        s = 0
        embed1=discord.Embed(title="__Available Linked Accounts !__", color=discord.Colour.random())
        embed2=discord.Embed(color=discord.Colour.random())
        embed3=discord.Embed(color=discord.Colour.random())
        embed4=discord.Embed(color=discord.Colour.random())
        for token in token_list:
            try:
                api = HQApi(token)
                data = api.get_users_me()
                username = data["username"]
                lives = data["items"]["lives"]
                superSpins = data["items"]["superSpins"]
                erasers = data["items"]["erase1s"]
                coins = data["coins"]
                api = HQApi(token)
                data = api.get_payouts_me()
                bal = data["balance"]
                total = bal["prizeTotal"]
                paid = bal["paid"]
                pending = bal["pending"]
                unpaid = bal["unpaid"]
                available = bal["available"]
                unclaimed = bal["frozen"]

                s = s + 1
                embed=discord.Embed(title=f"**Loading A/c(s)...({s})**", color=discord.Colour.random())
                await x.edit(embed=embed)
                if s < 21:
                    name = f"{s}. {username}"
                    value = f"<:extra_coins:844448578881847326> {coins}\n<:extra_life:844448511264948225> {lives}\n<:eraser:844448550498205736> {erasers}\n💰 {total} (Unclaimed : {unclaimed})\n💸 {available} ready for cashout."
                    embed1.add_field(name=name, value=value)
                elif s < 41:
                    name = f"{s}. {username}"
                    value = f"<:extra_coins:844448578881847326> {coins}\n<:extra_life:844448511264948225> {lives}\n<:eraser:844448550498205736> {erasers}\n💰 {total} (Unclaimed : {unclaimed})\n💸 {available} ready for cashout."
                    embed2.add_field(name=name, value=value)
                else:
                    name = f"{s}. {username}"
                    value = f"<:extra_coins:844448578881847326> {coins}\n<:extra_life:844448511264948225> {lives}\n<:eraser:844448550498205736> {erasers}\n💰 {total} (Unclaimed : {unclaimed})\n💸 {available} ready for cashout."
                    embed3.add_field(name=name, value=value)
            except:
                pass
        if s > 0:
            embed1.set_thumbnail(url=self.client.user.avatar_url)
            embed1.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await x.edit(embed=embed1)
        if s > 20:
            embed2.set_thumbnail(url=self.client.user.avatar_url)
            embed2.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed2)
        if s > 40:
            embed3.set_thumbnail(url=self.client.user.avatar_url)
            embed3.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed3)
        

def setup(client):
    client.add_cog(Profile(client))
