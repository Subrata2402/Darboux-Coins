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


class Cashout(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def payout(self, ctx, username=None):
        """Get recent payment details."""
        if username is None:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}payout [username]` to check your HQ account cashout details.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        commander_id = ctx.author.id
        name_list = []
        all_data = list(token_base.find({"id": commander_id, "username": username}))
        for i in all_data:
            name_list.append(i['username'])
        if username in name_list:
            token = token_base.find_one({'username': username})['token']
            try:
                api = HQApi(token)
                data = api.get_users_me()
            except ApiResponseError:
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please use Command `{ctx.prefix}refresh {username}` to refresh your account.", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            username = data["username"]
            api = HQApi(token)
            data = api.get_payouts_me()
            description_info = f""
            s = 0
            for data in data["payouts"]:
                s = int(s) + 1
                if s > 10:
                    break
                amount = data["amount"]
                email = data["targetEmail"]
                tim = data["created"]
                tm = aniso8601.parse_datetime(tim)
                x =  tm.strftime("%H:%M:%S [%d/%m/%Y] ")
                x_ind = tm.astimezone(timezone("Asia/Kolkata"))
                create_at = x_ind.strftime("%d-%m-%Y %I:%M %p")
                tim = data["modified"]
                tm = aniso8601.parse_datetime(tim)
                x =  tm.strftime("%H:%M:%S [%d/%m/%Y] ")
                x_ind = tm.astimezone(timezone("Asia/Kolkata"))
                modify_at = x_ind.strftime("%d-%m-%Y %I:%M %p")
                description_info += f"• Amount :** {amount}**\n• Email :** {email}**\n• Payment Created :** {create_at}**\n• Payment Completed :** {modify_at}**\n\n"
            await ctx.send("Details send in DM. Please check your DM!")
            embed=discord.Embed(title=f"**__Payout Summary of {username} !__**", description=description_info, color=discord.Colour.random())
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            await ctx.author.send(embed=embed)
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)


    @commands.command()
    async def cashout(self, ctx, email=None, username=None):
        """Make Cashout of an account."""
        if ctx.guild:
            embed=discord.Embed(title="⚠️ Direct Message Only", description="For the security of your HQ account, use that Command in DM only.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        if not email or not username:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}cashout [email] [username]` to cashout from your HQ Trivia account.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        commander_id = ctx.author.id
        channel = self.client.get_channel(841489919067029535)
        name_list = []
        all_data = list(token_base.find({"id": commander_id, "username": username}))
        for i in all_data:
            name_list.append(i['username'])
        if username in name_list:
            token = token_base.find_one({'username': username})['token']
            try:
                api = HQApi(token)
                data = api.get_users_me()
            except ApiResponseError:
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            try:
                data = requests.post(url="https://api-quiz.hype.space/users/me/payouts", headers={"Authorization": f"Bearer {token}"}, data={"email": email}).json()
            except Exception as e:
                error = e["error"]
                embed=discord.Embed(title="⚠️ Api Response Error", description=error, color=discord.Colour.random())
                return await ctx.send(embed=embed)
            print(data)
            data = data["data"]
            amount = data["amount"]
            email = data["targetEmail"]
            embed=discord.Embed(title="**Cashout Done ✅**", description=f"Successfully Cashout of Amount **{amount}** to PayPal Email **{email}**", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)
            await channel.send(f"**{ctx.author}** made a Successfully cashout of amount **{amount}**")
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)
            


def setup(client):
    client.add_cog(Cashout(client))
