import discord
import random
from discord.ext import commands
import asyncio
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from datetime import datetime
import datetime
from database.db import token_base, login_token_base
from discord_components import *


class Profile(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def accounts(self, ctx):
        commander_id = ctx.author.id
        check_id = token_base.find_one({"id": commander_id})
        if not check_id:
            embed=discord.Embed(title="❎ Not Found", description=f"You have not linked any of your accounts in the bot database.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        all_data = list(token_base.find({"id": commander_id}))
        name_list = [data.get("username") for data in all_data]
        name = ""
        for index, username in enumerate(name_list):
            name += f"{'0' if index+1 < 10 else ''}{index+1} - {username}\n"
        embed=discord.Embed(title=f"{ctx.author.name}'s accounts !", description = f"```\n{name}\n```", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def profile(self, ctx):
        commander_id = ctx.author.id
        check_id = login_token_base.find_one({"id": commander_id})
        if not check_id:
            embed=discord.Embed(title="❎ Not Found", description=f"You have not linked any of your accounts in the bot database.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        if ctx.guild:
            await ctx.send("Check your DM! Details send in DM's.")
        embed=discord.Embed(title="**Loading Your Accounts...**", color=discord.Colour.random())
        x = await ctx.author.send(embed=embed)
        all_data = list(login_token_base.find({"id": commander_id}))
        login_token_list = [data.get("login_token") for data in all_data]
        s = 0
        b = 0
        description = ""
        embed1=discord.Embed(title="__Available Linked Accounts !__", color=discord.Colour.random())
        embed2=discord.Embed(color=discord.Colour.random())
        embed3=discord.Embed(color=discord.Colour.random())
        for index, token in enumerate(login_token_list):
            try:
                api = HQApi()
                data = api.get_tokens(token)
                name = data["username"]
                user_id = data["userId"]
                access_token = data["accessToken"]
                update = ({'token': access_token})
                token_base.update_one({'user_id': user_id}, {'$set': update})
                update = ({'username': name})
                token_base.update_one({'user_id': user_id}, {'$set': update})
                login_token_base.update_one({'user_id': user_id}, {'$set': update})
                api = HQApi(access_token)
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
                embed=discord.Embed(title=f"**Loading Your Accounts... - {s}**", color=discord.Colour.random())
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
            except Exception as e:
                print(e)
                username = login_token_base.find_one({"login_token": token}).get("username")
                b = b + 1
                description += f"{b}. {username}\n"
        if s > 0:
            embed1.set_thumbnail(url=self.client.user.avatar_url)
            embed1.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await x.edit(embed=embed1)
        if s > 20:
            embed2.set_thumbnail(url=self.client.user.avatar_url)
            embed2.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.author.send(embed=embed2)
        if s > 40:
            embed3.set_thumbnail(url=self.client.user.avatar_url)
            embed3.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.author.send(embed=embed3)
        if b > 0:
            embed4=discord.Embed(title="⚠️ Expired Accounts", description=f"{description}\n\nThese account's tokens are expired. Please use `{ctx.prefix}refresh (username)` to refresh these accounts.", color=discord.Colour.random())
            embed4.set_thumbnail(url=self.client.user.avatar_url)
            embed4.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.author.send(embed=embed4)
        

def setup(client):
    client.add_cog(Profile(client))
