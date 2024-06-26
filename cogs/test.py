import discord
import random
from discord.ext import commands
import asyncio
from pymongo import MongoClient
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from HQApi import HQApi
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

data = MongoClient('mongodb+srv://Subrata2001:Subrata2001@cluster0.ywnwn.mongodb.net/MimirQuiz?retryWrites=true&w=majority')#Your Database Url
db = data.get_database("MimirQuiz")#Your db name
sb_details = db.sb_details

client = MongoClient("mongodb+srv://Subrata3250:subrata3250@cluster0.gqwt8.mongodb.net/Swagbucks?retryWrites=true&w=majority")
db = client.get_database("Swagbucks")
qt_base = db.sb_details

class DcPlay(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def qbackup(self, ctx):
        all_data = list(sb_details.find())
        for question in all_data:
            qt_base.insert_one(question)
        await ctx.send("success")

    @commands.command()
    async def set(self, ctx):
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjI3NDc3MDY0LCJ1c2VybmFtZSI6IlN1YnJhdGE5YjkxaGQiLCJhdmF0YXJVcmwiOiJodHRwczovL2Nkbi5wcm9kLmh5cGUuc3BhY2UvZGEvZ3JlZW4ucG5nIiwidG9rZW4iOiI4Vm1PTkciLCJyb2xlcyI6W10sImNsaWVudCI6IkFuZHJvaWQvMS41Mi4zIiwiZ3Vlc3RJZCI6bnVsbCwidiI6MSwiaWF0IjoxNjIxMzA1MzIxLCJleHAiOjE2MjkwODEzMjEsImlzcyI6Imh5cGVxdWl6LzEifQ.U_yCk2eayDDFRIcV9QciLe_fMHK09q8ihFVYRIsUaoY"
        api = HQApi(token)
        data = api.swipe()
        await ctx.send(data)

    @commands.command()
    async def dcp(self, ctx, username:str):
        """Play HQ Daily Challenge."""
        try:
            await ctx.message.delete()
        except:
            pass
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
        token = token_base.find_one({'username': username})['token']
        try:
            api = HQApi(token)
            data = api.get_users_me()
        except ApiResponseError:
            embed=discord.Embed(title="⚠️ Api Response Error", description=f"This account token is expired. Please refresh your account by this command.\n```\n{ctx.prefix}refresh (username)\n```", color=0x00ffff)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        coins = data["coins"]
        embed=discord.Embed(title="Playing HQ Offair Trivia...", color=0x00ffff)
        x = await ctx.send(embed=embed)
        username = "||Private Account||"
        q_list = []
        all_data = list(q_base.find())
        for i in all_data:
            q_list.append(i['question'])
        embed=discord.Embed(title="Playing HQ Offair Trivia...", description=f"**• Username : {username}\n• Games Played : 00\n• Questions Correct : 00/00\n• Coins Earned : 0\n• Total Coins : {coins}**", color=0x00ffff)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/773955381063974972.gif")
        await x.edit(embed=embed)
        try:
            offair_id = api.start_offair()['gameUuid']
        except ApiResponseError:
            offair_id = api.get_schedule()['offairTrivia']["waitTimeMs"]
            time=int(offair_id)/int(1000)
            milli=int(time)
            hours=(milli/(3600))
            hours=int(hours)
            minutes=((milli/(60))-(hours*(60)))
            minutes=int(minutes)
            seconds=((milli)-(hours*(3600))-(minutes*(60)))
            seconds=int(seconds)
            await asyncio.sleep(1)
            if hours <= 0:
                embed=discord.Embed(description=f"You have played all games as of now, so you must wait **{minutes}** minute(s) **{seconds}** second(s) to play Daily Challenge once again.", color=0x00ffff)
                await x.edit(embed=embed)
            else:
                embed=discord.Embed(description=f"You have played all games as of now, so you must wait **{hours}** hour(s) **{minutes}** minute(s) and **{seconds}** second(s) to play Daily Challenge once again.", color=0x00ffff)
                await x.edit(embed=embed)
            offair_id = api.get_schedule()['offairTrivia']['games'][0]['gameUuid']
        game_count = 0
        ct = 0
        coins = 0
        while True:
            #offair_id = api.start_offair()['gameUuid']
            offair = api.offair_trivia(offair_id)
            answers = [unidecode(ans["text"]) for ans in offair['question']['answers']]
            question=offair['question']['question']
            option1=f"{answers[0]}"
            option2=f"{answers[1]}"
            option3=f"{answers[2]}"
            
            if question in q_list:
                answer = q_base.find_one({'question': question})['answer']
                if option1 == answer:
                    select = 1
                elif option2 == answer:
                    select = 2
                else:
                    select = 3
            else:
                select = 2
            data = api.send_offair_answer(offair_id, offair['question']['answers'][select - 1]['offairAnswerId'])
            answer_counts = {}
            correct = ""
            for answer in data["answerCounts"]:
                ans_str = unidecode(answer["answer"])

                if answer["correct"]:
                    correct = ans_str
            qcnt = (offair['question']['questionNumber'])
            qs = int(0) + int(qcnt)
            if option1 == correct:
                check_if_exist = q_base.find_one({"question": question})
                if check_if_exist == None:
                    questions_and_answer = {'question': question,
                                            'answer': correct,
                                            'option':"1"}
                    q_base.insert_one(questions_and_answer)
                else:
                    print("Exist!")
                
            elif option2 == correct:
                check_if_exist = q_base.find_one({"question": question})
                if check_if_exist == None:
                    questions_and_answer = {'question': question,
                                            'answer': correct,
                                            'option':"2"}
                    q_base.insert_one(questions_and_answer)
                else:
                    print("Exist!")
                
            else:
                check_if_exist = q_base.find_one({"question": question})
                if check_if_exist == None:
                    questions_and_answer = {'question': question,
                                            'answer': correct,
                                            'option':"3"}
                    q_base.insert_one(questions_and_answer)
                else:
                    print("Exist!")
                
            if data['gameSummary']:
                tcoins = str(data['gameSummary']['coinsTotal'])
                coins = int(coins) + int(data['gameSummary']['coinsEarned'])
                ct = int(ct) + int(data['gameSummary']['questionsCorrect'])
                game_count = int(game_count) + 1
                qcn = int(game_count)*(12)
                embed=discord.Embed(title="Playing HQ Offair Trivia...", description=f"**• Username : {username}\n• Games Played : {game_count}\n• Questions Correct : {ct}/{qcn}\n• Coins Earned : {coins}\n• Total Coins : {tcoins}**", color=0x00ffff)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/773955381063974972.gif")
                await x.edit(embed=embed)
                break
        embed=discord.Embed(title="**Played HQ Offair Trivia ✅**", description=f"**• Username : {username}\n• Games Played : {game_count}\n• Questions Correct : {ct}/{qcn}\n• Coins Earned : {coins}\n• Total Coins : {tcoins}**", color=0x00ffff)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await x.edit(embed=embed)
        

def setup(client):
    client.add_cog(DcPlay(client))
