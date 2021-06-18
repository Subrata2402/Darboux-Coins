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
import DiscordUtils

data = MongoClient('mongodb+srv://Subrata2001:Subrata2001@cluster0.ywnwn.mongodb.net/Darboux?retryWrites=true&w=majority')#Your Database Url
db = data.get_database("Darboux")#Your db name
token_base = db.token
q_base = db.questions

class FbMethod(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def fbmethod(self, ctx):
        embed1=discord.Embed(title="**__Facebook Login Method__**", description=f"**Thanks {ctx.author.mention}, for using {self.client.user.mention} Bot. Follow these steps to add your HQ Trivia account with bot by Facebook.\n\nEnter `next` for get the process of Facebook Login Method.**", color=discord.Colour.random())
        

        embed2=discord.Embed(title="**__Step - 1__**", description=f"**Download Web Inspector (Open Source) Application from Google Play Store. [Click Here](https://play.google.com/store/apps/details?id=ai.agusibrahim.xhrlog) to redirect in Google Play Store.**", color=discord.Colour.random())
        embed2.set_image(url="https://cdn.discordapp.com/attachments/840841165544620062/843321573070864414/Screenshot_2021-05-16-08-28-35-77.jpg")
        embed2.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        embed2.timestamp = datetime.datetime.utcnow()

        embed3=discord.Embed(title="**__Step -2__**", description=f"**Use `{ctx.prefix}fblink` in DM to initiate login with Facebook. You will be sent a login link by the bot. Copy this link. Or, [Click Here](https://m.facebook.com/v9.0/dialog/oauth?auth_type=rerequest&cbt=1613638985174&client_id=1309867799121574&default_audience=friends&display=touch&e2e=%7B%22init%22%3A1596063.1199975831%7D&fbapp_pres=1&ies=0&nonce=EC40E5E9-148C-4D27-955B-54A3B8635F47&redirect_uri=fb1309867799121574%3A%2F%2Fauthorize%2F&response_type=id_token%2Ctoken_or_nonce%2Csigned_request%2Cgraph_domain&return_scopes=true&scope=email%2Copenid&sdk=ios&sdk_version=9.0.0&state=%7B%22challenge%22%3A%22weDSTppN3JYneIZMp63Vd71MOZ0%253D%22%2C%220_auth_logger_id%22%3A%22361441EC-F569-418B-9E84-E0703A60B519%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D) to get login link.**", color=discord.Colour.random())
        embed3.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        embed3.timestamp = datetime.datetime.utcnow()
        embed3.set_image(url="https://cdn.discordapp.com/attachments/838633900950552606/843324684274499624/IMG_20210516_084103.jpg")
        
        embed4=discord.Embed(title="**__Step - 3__**", description=f"**Open Web Inspector Application and click the `>` symbol and paste the link which you copied. Then search this link.**", color=discord.Colour.random())
        embed4.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        embed4.timestamp = datetime.datetime.utcnow()
        embed4.set_image(url="https://cdn.discordapp.com/attachments/838633900950552606/843326271567429642/IMG_20210516_084711.jpg")
        
        embed5=discord.Embed(title="**__Step - 4__**", description=f'**Facebook will ask you to sign in. Sign into your Facebook account which have linked in HQ Trivia. Then will say "You previously logged in to HQ with Facebook. Would you like to continue?" Select "Continue".**', color=discord.Colour.random())
        embed5.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        embed5.timestamp = datetime.datetime.utcnow()
        embed5.set_image(url="https://cdn.discordapp.com/attachments/838633900950552606/843329371322056704/Screenshot_2021-05-16-08-58-04-62_a9f4932b93b00310eaf049da0ec98783.jpg")
        
        embed6=discord.Embed(title="**__Step - 5__**", description=f'**You will get an error message saying "Web page not available". Click on the 3 dot icon and choose "Network Logs". You will get some links, copy the one which will start with `fb`.**', color=discord.Colour.random())
        embed6.set_image(url="https://cdn.discordapp.com/attachments/838633900950552606/843332123218018304/IMG_20210516_091037.jpg")
        embed6.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        embed6.timestamp = datetime.datetime.utcnow()
        
        embed7=discord.Embed(title="**__Step - 6__**", description=f"**Paste this in Notes and copy the fbtoken after from `access_token=` to before `&data_access`.**", color=discord.Colour.random())
        embed7.set_image(url="https://cdn.discordapp.com/attachments/838633900950552606/843336349901258752/IMG_20210516_092723.jpg")
        embed7.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        embed7.timestamp = datetime.datetime.utcnow()

        embed8=discord.Embed(title="**__Last Step__**", description=f"**Then use `{ctx.prefix}fblogin [fbtoken]` and successfully add your account in bot database. Use `{ctx.prefix}accounts` to check your saved accounts.**", color=0x00ffff)
        embed8.set_image(url="https://cdn.discordapp.com/attachments/838633900950552606/843353243500150794/IMG_20210516_103423.jpg")
        embed8.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        embed8.timestamp = datetime.datetime.utcnow()

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
    client.add_cog(FbMethod(client))