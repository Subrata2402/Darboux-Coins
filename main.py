import re
import discord
from discord.ext import commands
from discord.ext.commands import bot
import asyncio
import datetime
from itertools import cycle
import time
import platform
import colorsys
import random
import os
import sys
import traceback
import json

from pymongo import MongoClient

data = MongoClient('mongodb+srv://Subrata2001:Subrata2001@cluster0.ywnwn.mongodb.net/Darboux?retryWrites=true&w=majority')#Your Database Url
db = data.get_database("Darboux")#Your db name
pre_base = db.prefix
link_base = db.antilinks

bot_prefix = commands.when_mentioned_or("-","+")


intents = discord.Intents.all()
client = commands.Bot(command_prefix = bot_prefix, intents=intents)
client.remove_command('help')

@client.event
async def on_ready():
    print('====================')
    print(client.user)
    channel = client.get_channel(835743589241454592)
    embed=discord.Embed(title="Bot Updated ✅", description="Bot successfully updated. No issues found!", color=0x00ffff)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.set_footer(text=client.user, icon_url=client.user.avatar_url)
    await channel.send(embed=embed)
    while True:
        await client.change_presence(activity=discord.Activity(type=3,name="on "+str(len(client.guilds))+" servers | -invite"))
        await asyncio.sleep(5)
        await client.change_presence(status=discord.Status.idle, activity=discord.Game(name="with -dcplay <username>", type=2))
        await asyncio.sleep(5)
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name="with Help ➜ -help", type=2))
        await asyncio.sleep(5)
        await client.change_presence(status=discord.Status.online, activity=discord.Game(name="with -addtoken <token>", type=2))
        await asyncio.sleep(5)

@client.event
async def on_message(msg):
   if msg.content.startswith(client.user.mention):
       await msg.channel.send("My prefix is +")
   await client.process_commands(msg)

@client.command()
@commands.has_permissions(administrator=True)
async def say(ctx, *, msg):
    await ctx.message.delete()
    await ctx.send(msg)
    
@client.command()
@commands.has_permissions(administrator=True)
async def sayem(ctx, *, msg):
    await ctx.message.delete()
    embed=discord.Embed(description=msg, color=0x00ffff)
    await ctx.send(embed=embed)

@client.command(pass_context=True,aliases=['pong'])
async def ping(ctx):
    """ Pong! """
    before = time.monotonic()
    message = await ctx.send("**__Pong!__**")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"**__Pong!__** :ping_pong:  **{int(ping)}ms**")
    print(f'Ping {int(ping)}ms')


extensions = [
              "cogs.login", "cogs.show", "cogs.hqname", "cogs.welcome",
              "cogs.logintoken", "cogs.token", "cogs.payout", "cogs.dcplay",
              "cogs.editname", "cogs.userinfo", "cogs.details", "cogs.help",
              "cogs.rwin", "cogs.refresh", "cogs.friend", "cogs.sdcplay",
              "cogs.fblogin", "cogs.glogin", "cogs.test"
]
if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            print(f"Error loading {extension}", file=sys.stderr)
            traceback.print_exc()




token = "ODI1OTU1OTEzMDcyNTA4OTY5.YGFdYw.3muixu2dRjoKEx7kLdFCPHke8wE"
client.run(token)
