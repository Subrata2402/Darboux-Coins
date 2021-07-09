import discord
import random
from discord.ext import commands
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
from database.db import token_base, login_token_base


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
            embed=discord.Embed(title="❎ Not Found", description=f"You have not added any of your accounts in bot database.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        if ctx.guild:
            await ctx.send(f"{ctx.author.mention}, **Check your DM!**")
        embed=discord.Embed(title="Fetching your account balance and Cashout details...", color=0x00ffff)
        x = await ctx.author.send(embed=embed)
        description = ""
        total = 0
        paid = 0
        pending = 0
        unpaid = 0
        available = 0
        sl_no = 0
        ex_no = 0
        for username in name_list:
            token = token_base.find_one({'username': username})['token']
            try:
                api = HQApi(token)
                data = api.get_payouts_me()
                bal = data["balance"]
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
                sl_no = int(sl_no) + 1
                embed=discord.Embed(title=f"**__Balance & Cashout Details of {sl_no} Accounts :__-**", description=f"**• Total Balance :** ${total} 💰\n**• Claimed Ammount :** ${paid} 💸\n**• Pending Ammount :** ${pending} 💰\n**• Unclaimed Ammount :** ${unpaid} 💸\n**• Available for Cashout :** ${available} 💰", color=discord.Colour.random())
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/844442503976583178.gif")
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await x.edit(embed=embed)
            except:
                ex_no = int(ex_no) + 1
                description += f"{ex_no} - {username}\n"
        embed=discord.Embed(title=f"**__Balance & Cashout Details of {sl_no} Accounts :__-**", description=f"**• Total Balance :** ${total} 💰\n**• Claimed Ammount :** ${paid} 💸\n**• Pending Ammount :** ${pending} 💰\n**• Unclaimed Ammount :** ${unpaid} 💸\n**• Available for Cashout :** ${available} 💰", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await x.edit(embed=embed)
        if ex_no > 0:
            embed=discord.Embed(title="⚠️ Token Expired", description=f"{description}\nThis account's tokens are expired. Please refresh your accounts to use this command `{ctx.prefix}refresh <username>`", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.author.send(embed=embed)
        else:
            return

def setup(client):
    client.add_cog(Details(client))
