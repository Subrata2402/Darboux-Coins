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
        page1 = discord.Embed(color=discord.Colour.random())
        page1.add_field(name=f"**{ctx.prefix}add +(country code)(number)**", value="> To save your HQ Trivia account in bot.")
        page1.add_field(name=f"**{ctx.prefix}addtoken (token)**", value="> Add your HQ Trivia account in bot with token.")
        page1.add_field(name=f"**{ctx.prefix}fblink**", value="> Get Facebook Login Link.")
        page1.add_field(name=f"**{ctx.prefix}fblogin (fbtoken)**", value="> Add your HQ Trivia account in bot with Facebook token.")
        page1.add_field(name=f"**{ctx.prefix}dcplay (username)**", value="> Play HQ Trivia Daily Challenge and wins 48/48 to get you 400 <:extra_coins:844448578881847326> Coins.")
        page1.add_field(name=f"**{ctx.prefix}sdcplay (username)**", value="> Play HQ Trivia Daily Challenge in Slowmode and wins 48/48 to get you 400 <:extra_coins:844448578881847326> Coins.")
        page1.set_thumbnail(url=self.client.user.avatar_url)
        page1.set_author(name="| Darboux Coins Help Menu !", icon_url=self.client.user.avatar_url)
        page1.set_footer(text=f"Page : 01/05 | Total Commands : 06", icon_url=ctx.author.avatar_url)

        page2 = discord.Embed(color=discord.Colour.random())
        page2.add_field(name=f"**{ctx.prefix}accounts**", value="> To check, how many accounts you have added in the bot.")
        page2.add_field(name=f"**{ctx.prefix}token (username)**", value="> Get access token of your HQ account.")
        page2.add_field(name=f"**{ctx.prefix}details (username)**", value="> Get details of your HQ Trivia account.")
        page2.add_field(name=f"**{ctx.prefix}hquser (username)**", value="> Get any HQ user's info.")
        page2.add_field(name=f"**{ctx.prefix}remove (username)**", value="> Remove your HQ Trivia account from the bot database.")
        page2.add_field(name=f"**{ctx.prefix}removeall**", value="> Remove all saved accounts from bot database.")
        page2.add_field(name=f"**{ctx.prefix}refresh (username)**", value="> Refresh your HQ account if token is expired.")
        page2.add_field(name=f"**{ctx.prefix}recentwins (username)**", value="> Get last 30 winnings of your HQ account.")
        page2.set_thumbnail(url=self.client.user.avatar_url)
        page2.set_author(name="| Darboux Coins Help Menu !", icon_url=self.client.user.avatar_url)
        page2.set_footer(text=f"Page : 02/05 | Total Commands : 08", icon_url=ctx.author.avatar_url)

        page3 = discord.Embed(color=discord.Colour.random())
        page3.add_field(name=f"{ctx.prefix}life (username) [amount]", value="> Purchase Extra <:extra_life:844448511264948225> Life using <:extra_coins:844448578881847326> Coins.")
        page3.add_field(name=f"{ctx.prefix}eraser (username) [amount]", value="> Purchase Extra <:eraser:844448550498205736> Eraser using <:extra_coins:844448578881847326> Coins.")
        page3.add_field(name=f"{ctx.prefix}superspin (username) [amount]", value="> Purchase Extra <:super_spin:844448472908300299> Super-spin using <:extra_coins:844448578881847326> Coins.")
        page3.add_field(name=f"{ctx.prefix}swipe (username)", value="> Swiped your HQ account to earn an Extra <:extra_life:844448511264948225> Life.")
        page3.add_field(name=f"{ctx.prefix}cashout (email_id) (username)", value="> 💸 Cashout your winnings in your paypal account.")
        page3.add_field(name=f"{ctx.prefix}payout (username)", value="> Get last 10 💸 cashout details of your HQ account.")
        page3.add_field(name=f"{ctx.prefix}balance", value="> Get total 💰 balance & 💸 cashout details of all accounts.")
        page3.set_thumbnail(url=self.client.user.avatar_url)
        page3.set_author(name="| Darboux Coins Help Menu !", icon_url=self.client.user.avatar_url)
        page3.set_footer(text=f"Page : 03/05 | Total Commands : 07", icon_url=ctx.author.avatar_url)

        page4 = discord.Embed(color=discord.Colour.random())
        page4.add_field(name=f"{ctx.prefix}addfriend (username) (friend's username)", value="> Send friend request.")
        page4.add_field(name=f"{ctx.prefix}editname (username) (new_name)", value="> Edit your HQ account username.")
        page4.add_field(name=f"{ctx.prefix}friends (username)", value="> Get your HQ friends list.")
        page4.add_field(name=f"{ctx.prefix}acceptfriend (username) (friend's username)", value="> Accept friend request.")
        page4.add_field(name=f"{ctx.prefix}removefriend (username) (friend's username)", value="> Remove a friend from your friends list.")
        page4.add_field(name=f"{ctx.prefix}friendstatus (username) (friend's username)", value="> Check your friend's status.")
        page4.add_field(name=f"{ctx.prefix}hqname", value="> Get random US Name for HQ.")
        page4.add_field(name=f"{ctx.prefix}nextshow", value="> Get HQ Next Show details.")
        page4.set_thumbnail(url=self.client.user.avatar_url)
        page4.set_author(name="| Darboux Coins Help Menu !", icon_url=self.client.user.avatar_url)
        page4.set_footer(text=f"Page : 04/05 | Total Commands : 08", icon_url=ctx.author.avatar_url)

        page5 = discord.Embed(color=discord.Colour.random())
        page5.add_field(name=f"{ctx.prefix}report (message)", value="> Report your issues.")
        page5.add_field(name=f"{ctx.prefix}suggest (message)", value="> Suggest your suggestion.")
        page5.add_field(name=f"{ctx.prefix}feedback (message)", value="> Give your feedback.")
        page5.add_field(name=f"{ctx.prefix}botinfo", value="> Get the information about bot.")
        page5.add_field(name=f"{ctx.prefix}invite", value="> Invite bot in your server.")
        page5.add_field(name=f"{ctx.prefix}join", value="> Join our official bot server.")
        page5.set_thumbnail(url=self.client.user.avatar_url)
        page5.set_author(name="| Darboux Coins Help Menu !", icon_url=self.client.user.avatar_url)
        page5.set_footer(text=f"Page : 05/05 | Total Commands : 06", icon_url=ctx.author.avatar_url)

        pages = [page1, page2, page3, page4, page5]

        message = await ctx.send(embed = page1)
        await message.add_reaction('⏮')
        await message.add_reaction('◀')
        await message.add_reaction('▶')
        await message.add_reaction('⏭')

        def check(reaction, user):
            return user == ctx.author

        i = 0
        reaction = None

        while True:
            if str(reaction) == '⏮':
                i = 0
                await message.edit(embed = pages[i])
            elif str(reaction) == '◀':
                if i > 0:
                    i -= 1
                    await message.edit(embed = pages[i])
            elif str(reaction) == '▶':
                if i < 4:
                    i += 1
                    await message.edit(embed = pages[i])
            elif str(reaction) == '⏭':
                i = 4
                await message.edit(embed = pages[i])
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout = 60.0, check = check)
                try:
                    await message.remove_reaction(reaction, user)
                except:
                    pass
            except:
                break
        try:
            await message.clear_reactions()
        except:
            print("Don't have permission to remove reactions.")





def setup(client):
    client.add_cog(Help(client))
