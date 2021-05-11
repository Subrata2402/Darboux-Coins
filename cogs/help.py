import discord
import random
from discord.ext import commands
import asyncio

import asyncio

import requests
import json
import time
import colorsys
import datetime





class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        embed=discord.Embed(color=0x00ff00)
        embed.add_field(name=f"{ctx.prefix}add +(country code)(number)", value="To save your HQ Trivia account in bot.")
        embed.add_field(name=f"{ctx.prefix}dcplay (username)", value="Play HQ Trivia Daily Challenge.")
        embed.add_field(name=f"{ctx.prefix}sdcplay (username)", value="Play HQ Trivia Daily Challenge in Slowmode.")
        embed.add_field(name=f"{ctx.prefix}token (username)", value="Get access token of your HQ account.")
        embed.add_field(name=f"{ctx.prefix}addtoken (token)", value="Add your HQ Trivia account in bot by token.")
        embed.add_field(name=f"{ctx.prefix}remove (username)", value="Remove your HQ Trivia account from the bot.")
        embed.add_field(name=f"{ctx.prefix}refresh (username)", value="Refresh your HQ account if token is expired.")
        embed.add_field(name=f"{ctx.prefix}accounts", value="To check, how many accounts you have added in the bot.")
        embed.add_field(name=f"{ctx.prefix}details (username)", value="Get details of your HQ Trivia account.")
        embed.add_field(name=f"{ctx.prefix}recentwins (username)", value="Get recent some winnings of your HQ account.")
        embed.add_field(name=f"{ctx.prefix}cashout (email_id) (username)", value="Cashout your winnings in your paypal account.")
        embed.add_field(name=f"{ctx.prefix}hquser (username)", value="Get any HQ user's info.")
        embed.add_field(name=f"{ctx.prefix}payout (username)", value="Get some cashout details of your HQ account.")
        embed.add_field(name=f"{ctx.prefix}addfriend (username) (friend name)", value="Send friend request.")
        embed.add_field(name=f"{ctx.prefix}editname (username) (new_name)", value="Edit your HQ account username.")
        embed.add_field(name=f"{ctx.prefix}friends (username)", value="Get your HQ friends list.")
        #embed.add_field(name=f"{ctx.prefix}hqname", value="Get random US Name for HQ.")
        embed.add_field(name=f"{ctx.prefix}nextshow", value="Get HQ Next Show details.")
        embed.add_field(name="Important Links:", value="[Invite Bot](https://discord.com/api/oauth2/authorize?client_id=838631852603474001&permissions=523376&scope=bot) | [Support Server](https://discord.gg/TAcEnfS8Rs)")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_author(name="| Darboux Coins Help Menu !", icon_url=self.client.user.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.timestamp = (datetime.datetime.utcnow())
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        embed=discord.Embed(title="**Invite Me to Your Server !**", description="**Invite Link : [Click Here](https://discord.com/api/oauth2/authorize?client_id=838631852603474001&permissions=523376&scope=bot)**", color=0x00ffff)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def support(self, ctx):
        embed=discord.Embed(title="**Join Our Support Server !**", description="**Join Link : [Click Here](https://discord.gg/TAcEnfS8Rs)**", color=0x00ffff)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))
