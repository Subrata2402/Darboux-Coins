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


class Items(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def life(self, ctx, username=None, amount=None):
        """Purchase Life."""
        if not username:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}life [username] (amount)` to purchase an Extra Life in your HQ Trivia account.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        commander_id = ctx.author.id
        name_list = []
        all_data = list(token_base.find({"id": commander_id, "username": username}))
        for i in all_data:
            name_list.append(i['username'])
        if username not in name_list:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        token = token_base.find_one({'username': username})['token']
        try:
            api = HQApi(token)
            data = api.get_users_me()
            coins = data["coins"]
            erasers = data["items"]["erase1s"]
            superSpins = data["items"]["superSpins"]
        except ApiResponseError:
            embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        headers = {"Authorization": f"Bearer {token}"}
        if not amount:
            if coins < 400:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient coins to purchase 1 <:life:844142423524245524> Extra Life. Play HQ Daily Challenge and earn some coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            r = requests.post("https://api-quiz.hype.space/store/com.intermedia.hq.item.extralife.1x/purchase", headers=headers)
            data = r.json()
            coins = data["coinsTotal"]
            life = data["itemsTotal"]["extra-life"]
            embed=discord.Embed(title="Life Purchased ✅", description=f"You have successfully purchased an <:life:844142423524245524> Extra Life!\n\n**• Total Coins :** {coins}\n**• Total Lives :** {life}\n**• Total Erasers :** {erasers}\n**• Total Super-spins :** {superSpins}", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        try:
            amount = int(amount)
        except:
            return await ctx.send(f"{amount} is not a valid amount.")
        if amount == int(1):
            if coins < 400:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient coins to purchase 1 <:life:844142423524245524> Extra Life. Play HQ Daily Challenge and earn some coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
        elif amount == int(3):
            if coins < 1000:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient coins to purchase 3 <:life:844142423524245524> Extra Lifes. Play HQ Daily Challenge and earn some coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
        elif amount == int(5):
            if coins < 1500:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient coins to purchase 5 <:life:844142423524245524> Extra Lifes. Play HQ Daily Challenge and earn some coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="⚠️ Api Response Error", description=f"You can't purchase {amount} <:life:844142423524245524> Extra Life(s). Please choose an amount between 1, 3 and 5.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        r = requests.post(f"https://api-quiz.hype.space/store/com.intermedia.hq.item.extralife.{amount}x/purchase", headers=headers)
        data = r.json()
        coins = data["coinsTotal"]
        life = data["itemsTotal"]["extra-life"]
        embed=discord.Embed(title="Life Purchased ✅", description=f"You have successfully purchased {amount} <:life:844142423524245524> Extra Life(s)!\n\n**• Total Coins :** {coins}\n**• Total Lives :** {life}\n**• Total Erasers :** {erasers}\n**• Total Super-spins :** {superSpins}", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def eraser(self, ctx, username=None, amount=None):
        """Purchase Eraser."""
        if not username:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}eraser [username] (amount)` to purchase an Extra Eraser in your HQ Trivia account.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        commander_id = ctx.author.id
        name_list = []
        all_data = list(token_base.find({"id": commander_id, "username": username}))
        for i in all_data:
            name_list.append(i['username'])
        if username not in name_list:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        token = token_base.find_one({'username': username})['token']
        try:
            api = HQApi(token)
            data = api.get_users_me()
            coins = data["coins"]
            life = data["items"]["lives"]
            superSpins = data["items"]["superSpins"]
        except ApiResponseError:
            embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        headers = {"Authorization": f"Bearer {token}"}
        if not amount:
            if coins < 100:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient coins to purchase 1 <:eraser:844142457955549195> Extra Eraser. Play HQ Daily Challenge and earn some coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            r = requests.post(f"https://api-quiz.hype.space/store/com.intermedia.hq.item.erasers.1x/purchase", headers=headers)
            data = r.json()
            coins = data["coinsTotal"]
            erasers = data["itemsTotal"]["eraser"]
            embed=discord.Embed(title="Eraser Purchased ✅", description=f"You have successfully purchased an <:eraser:844142457955549195> Extra Eraser!\n\n**• Total Coins :** {coins}\n**• Total Lives :** {life}\n**• Total Erasers :** {erasers}\n**• Total Super-spins :** {superSpins}", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        try:
            amount = int(amount)
        except:
            return await ctx.send(f"{amount} is not a valid amount.")
        if amount == int(1):
            if coins < 100:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient coins to purchase 1 <:eraser:844142457955549195> Extra Eraser. Play HQ Daily Challenge and earn some coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
        elif amount == int(3):
            if coins < 250:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient coins to purchase 3 <:eraser:844142457955549195> Extra Erasers. Play HQ Daily Challenge and earn some coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
        elif amount == int(5):
            if coins < 400:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient coins to purchase 5 <:eraser:844142457955549195> Extra Erasers. Play HQ Daily Challenge and earn some coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="⚠️ Api Response Error", description=f"You can't purchase {amount} <:eraser:844142457955549195> Extra Eraser(s). Please choose an amount between 1, 3 and 5.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        r = requests.post(f"https://api-quiz.hype.space/store/com.intermedia.hq.item.erasers.{amount}x/purchase", headers=headers)
        data = r.json()
        coins = data["coinsTotal"]
        erasers = data["itemsTotal"]["eraser"]
        embed=discord.Embed(title="Eraser Purchased ✅", description=f"You have successfully purchased {amount} <:eraser:844142457955549195> Extra Eraser(s)!\n\n**• Total Coins :** {coins}\n**• Total Lives :** {life}\n**• Total Erasers :** {erasers}\n**• Total Super-spins :** {superSpins}", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def superspin(self, ctx, username=None, amount=None):
        """Purchase superspin."""
        if not username:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}superspin [username] (amount)` to purchase an Extra Super-spin in your HQ Trivia account.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        commander_id = ctx.author.id
        name_list = []
        all_data = list(token_base.find({"id": commander_id, "username": username}))
        for i in all_data:
            name_list.append(i['username'])
        if username not in name_list:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        token = token_base.find_one({'username': username})['token']
        try:
            api = HQApi(token)
            data = api.get_users_me()
            coins = data["coins"]
            erasers = data["items"]["erase1s"]
            life = data["items"]["lives"]
            superSpins = data["items"]["superSpins"]
        except ApiResponseError:
            embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        headers = {"Authorization": f"Bearer {token}"}
        if not amount:
            if coins < 150:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient coins to purchase 1 Extra Super-spin. Play HQ Daily Challenge and earn some coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            r = requests.post("https://api-quiz.hype.space/store/com.intermedia.hq.item.superspin.1x/purchase", headers=headers)
            data = r.json()
            coins = data["coinsTotal"]
            superSpins = int(superSpins) + 1
            embed=discord.Embed(title="Super-spin Purchased ✅", description=f"You have successfully purchased an Extra Super-spin!\n\n**• Total Coins :** {coins}\n**• Total Lives :** {life}\n**• Total Erasers :** {erasers}\n**• Total Super-spins :** {superSpins}", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        try:
            amount = int(amount)
        except:
            return await ctx.send(f"{amount} is not a valid amount.")
        if amount == int(1):
            if coins < 150:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient coins to purchase 1 Extra Super-spin. Play HQ Daily Challenge and earn some coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
        elif amount == int(3):
            if coins < 400:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient coins to purchase 3 Extra Super-spins. Play HQ Daily Challenge and earn some coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
        elif amount == int(5):
            if coins < 600:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient coins to purchase 5 Extra Super-spins. Play HQ Daily Challenge and earn some coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="⚠️ Api Response Error", description=f"You can't purchase {amount} Extra Super-spin(s). Please choose an amount between 1, 3 and 5.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        r = requests.post(f"https://api-quiz.hype.space/store/com.intermedia.hq.item.superspin.{amount}x/purchase", headers=headers)
        data = r.json()
        coins = data["coinsTotal"]
        superSpins = int(superSpins) + int(amount)
        embed=discord.Embed(title="Super-spin Purchased ✅", description=f"You have successfully purchased {amount} Extra Super-spin(s)!\n\n**• Total Coins :** {coins}\n**• Total Lives :** {life}\n**• Total Erasers :** {erasers}\n**• Total Super-spins :** {superSpins}", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Items(client))
