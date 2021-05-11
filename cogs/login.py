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
import re

data = MongoClient('mongodb+srv://Subrata2001:Subrata2001@cluster0.ywnwn.mongodb.net/Darboux?retryWrites=true&w=majority')#Your Database Url
db = data.get_database("Darboux")#Your db name
token_base = db.token
login_token_base = db.login_token
number_base = db.number

def rand():
    ran = random.randint(3,12)
    x = "1234567890"
    y = "1234567890"
    uname = ""
    for i in range(ran):
      first = random.choice(("Aingge", "Alhiz", "tanhis", "jabnis", "Hamgish", "jsvjks", "Dayvid", "sognia", "Amyg", "Andya", "Aryda", "Aydun", "Bfhay", "Cgkia", "laidsre", "Clfjor", "Corfja", "Coruco", "Daruwn", "Flefjur", "Evfha", "Ettgja", "Eryrin", "Rotjbin", "Dagjn","Cafhmil","Rintugo","Cfhayli","Difhgna","Efgmma","Gghalen","Helgjma","Jancgje","Grefhtl","Hazgjel","Gwven","Helgen","Ellha","Ehdie",'Igjvy'))
    second = random.choice(("Jill", "Joss", "Juno", "Kady", "Kai", "Kira", "Klara", "germni", "haba", "janis", "Lana", "Leda", "Liesl", "Lily", "Amaa", "Mae", "Lula", "Lucia", "Mia", "Myra", "Opal", "Paige", "Rain", "Quinn", "Rose", "Sia", "Taya", "Teva", "markus", "Judie", "Zuri", "Zoe", "Vera", "Una", "Reeve",'Ekta'))
    c = random.choice(("1", "2", "3"))
    if c == "1":uname = first + second
    elif c == "2":uname = first.title() + second.title()
    elif c == "3": uname = first + second.title()
    d = random.choice(x)
    e = random.choice(y)
    name = uname+d+e
    api = HQApi()
    check = api.check_username(name)
    if not check:
        return name
    else:
        return rand()

class Login(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def add(self, ctx, number:str=None):
        """Add account using number and OTP."""
        if number is None:
            embed=discord.Embed(title="⚠️ Invalid Argument", description=f"You didn't write number after `{ctx.prefix}add`. Please correct use Command.\n`{ctx.prefix}add +<country code><number>`\nExample: `{ctx.prefix}add +13158686534`", color=0x00ffff)
            #embed.add_field(name="Usage :", value=f"{ctx.prefix}add +<country code><number>")
            #embed.add_field(name="Example :", value=f"{ctx.prefix}add +13158686534")
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        try:
            await ctx.message.delete()
        except:
            pass
        def replace(term):
            if len(term.group(0)) == 12:  # UserID
                return term.group(0)[:4]+ '*****' + term.group(0)[-3:]
            elif len(term.group(0)) == 11:  # Mobile
                return term.group(0)[:4]+ '****' + term.group(0)[-3:]
            elif len(term.group(0)) == 13:  # Mobile
                return term.group(0)[:4]+ '******' + term.group(0)[-3:]
            else:
                return term.group(0)
        s = number
        s_hide = re.sub('\d+', replace, s)
        commander_id = ctx.message.author.id
        api = HQApi()
        try:
            verification = api.send_code("+" + number, "sms")
            embed=discord.Embed(title="OTP Sent ✅", description=f"Successfully a 6-digits OTP has been sent to your number `{s_hide}` via SMS.\nEnter the OTP within 180 seconds.", color=0x00ffff)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            x = await ctx.send(embed=embed)
        except:
            embed=discord.Embed(title="⚠️ Exception Error", description="This is not a valid mobile number or some error occured while adding your account! Please try again later.", color=0x00ffff)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        def check(m):
            return m.author == ctx.message.author and m.channel == ctx.message.channel
        try:
            response = await self.client.wait_for('message',check= check, timeout=180)
            try:
                code = int(response.clean_content)
                sub_code_res = api.confirm_code(verification["verificationId"], code)
                name = rand()
                print(name)
                channel = ctx.channel
                while True:
                    try:
                        token = api.register(verification["verificationId"], name)
                        break
                    except Exception as e:
                        await x.edit(content=e)
                a_token = token["accessToken"]
                login_token = token ["loginToken"]
                api = HQApi(a_token)
                data = api.get_users_me()
                username = data["username"]
                id = data["userId"]
                check = token_base.find_one({"id": commander_id, "user_id": id})
                if check != None:
                    embed=discord.Embed(title="⚠️ Already Exists", description="This account already exists in bot database. You can't add it again.", color=0x00ffff)
                    embed.set_thumbnail(url=self.client.user.avatar_url)
                    embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                    return await x.edit(embed=embed)
                number_dict = {'id': commander_id,
                               'login_token': login_token,
                               'access_token': a_token,
                               'username': username,
                               'user_id': id}
                login_token_base.insert_one(number_dict)
                user_info_dict = {'id': commander_id,
                                  'token': a_token,
                                  'username': username, 'user_id': id}
                token_base.insert_one(user_info_dict)
                hide_name = "****" + username[4:]
                embed=discord.Embed(title="Account Added ✅", description=f"Successfully linked an account with name `{hide_name}`. Check your DM for more details!", color=0x00ff00)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await x.edit(embed=embed)
                embed=discord.Embed(description=f"Hey {ctx.author.name} you have successfully linked an account with name `{username}` Use `+dcplay {username}` to play HQ Trivia Daily Challenge. For more details use `+help`", color=0x00ff00)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await ctx.author.send(embed=embed)
                channel = self.client.get_channel(841489971109560321)
                await channel.send(f"**{ctx.author}** add an account via number and OTP.")
            except:
                em = discord.Embed(title="❎ Incorrect Code", description="Entered code is incorrect. If you want to login then restart this session once again.", color=0x00a8ff)
                em.set_thumbnail(url=self.client.user.avatar_url)
                em.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await x.edit(embed=em)
        except asyncio.TimeoutError:
            em = discord.Embed(title="⚠️ Time Out Error", description="Session timed out, you didn't enter the OTP in time. If you want to login then restart this session once again.", color=0x00a8ff)
            em.set_thumbnail(url=self.client.user.avatar_url)
            em.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await x.edit(embed=em)
            
        
        
    @add.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, Exception):
            await ctx.send(f'<@{ctx.author.id}> ```\n{error}\n```')

    @commands.command()
    async def remove(self, ctx, username:str):
        """Remove account from database."""
        commander_id = ctx.author.id
        name_list = []
        all_data = list(token_base.find({"id": commander_id, "username": username}))
        for i in all_data:
            name_list.append(i['username'])
        if username not in name_list:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=0x00ffff)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        number_dict = {'id': commander_id,
                       'username': username}
        login_token_base.delete_one(number_dict)
        user_info_dict = {'id': commander_id,
                          'username': username}
        token_base.delete_one(user_info_dict)
        embed=discord.Embed(title="Account Removed", description=f"Successfully removed an account from bot database with name `{username}`", color=0x00ff00)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Login(client))
