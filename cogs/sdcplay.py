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
q_base = db.questions

class DcPlay(commands.Cog):

    def __init__(self, client):
        self.client = client

    

    @commands.command(aliases=["splay"])
    async def sdcplay(self, ctx, username:str):
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
            embed=discord.Embed(title="⚠️ Token Expired", description=f"This account token is expired. Please use Command `{ctx.prefix}refresh {username}` to refresh your account.", color=0x00ffff)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        coins = data["coins"]
        embed=discord.Embed(title="Playing HQ Offair Trivia...", color=0x00ffff)
        x = await ctx.send(embed=embed)
        username = "||Private Account||"
        embed=discord.Embed(title="Playing HQ Offair Trivia...", description=f"**• Username : {username}\n• Games Played : 00\n• Questions Correct : 00/00\n• Coins Earned : 0\n• Total Coins : {coins}**", color=0x00ffff)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/773955381063974972.gif")
        await x.edit(embed=embed)
        q_list = []
        all_data = list(q_base.find())
        for i in all_data:
            q_list.append(i['question'])
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
        while True:
            offair = api.offair_trivia(offair_id)
            answers = [unidecode(ans["text"]) for ans in offair['question']['answers']]
            question=offair['question']['question']
            option1=f"{answers[0]}"
            option2=f"{answers[1]}"
            option3=f"{answers[2]}"
            await asyncio.sleep(2)
            if question in q_list:
                option = q_base.find_one({'question': question})['option']
                select = int(option)
            else:
                select = int(2)
            data = api.send_offair_answer(offair_id, offair['question']['answers'][select - 1]['offairAnswerId'])
            #print(data)
            answer_counts = {}
            correct = ""
            for answer in data["answerCounts"]:
                ans_str = unidecode(answer["answer"])

                if answer["correct"]:
                    correct = ans_str
            coins = str(data["coinsEarned"])
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
                coins = str(data['gameSummary']['coinsEarned'])
                correct = str(data['gameSummary']['questionsCorrect'])
                embed=discord.Embed(title="Playing HQ Offair Trivia...", description=f"**• Username : {username}\n• Games Played : 01\n• Questions Correct : {correct}/12\n• Coins Earned : {coins}\n• Total Coins : {tcoins}**", color=0x00ffff)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/773955381063974972.gif")
                await x.edit(embed=embed)
                break
        coins1 = int(coins)
        correct1 = int(correct)
        try:
            offair_id = api.start_offair()['gameUuid']
        except ApiResponseError:
            embed=discord.Embed(title="**Played Offair Trivia ✅**", description=f"**• Username : {username}\n• Games Played : 01\n• Questions Correct : {correct1}/12\n• Coins Earned : {coins1}\n• Total Coins : {tcoins}**", color=0x00ffff)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            await x.edit(embed=embed)
        while True:
            offair = api.offair_trivia(offair_id)
            answers = [unidecode(ans["text"]) for ans in offair['question']['answers']]
            question=offair['question']['question']
            option1=f"{answers[0]}"
            option2=f"{answers[1]}"
            option3=f"{answers[2]}"
            await asyncio.sleep(2)
            if question in q_list:
                option = q_base.find_one({'question': question})['option']
                select = int(option)
            else:
                select = int(2)
            data = api.send_offair_answer(offair_id, offair['question']['answers'][select - 1]['offairAnswerId'])
            #print(data)
            answer_counts = {}
            correct = ""
            for answer in data["answerCounts"]:
                ans_str = unidecode(answer["answer"])

                if answer["correct"]:
                    correct = ans_str
            coins = str(data["coinsEarned"])
            qcnt = (offair['question']['questionNumber'])
            qs = int(12) + int(qcnt)
            s = coins1
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
                coins = str(data['gameSummary']['coinsEarned'])
                correct = str(data['gameSummary']['questionsCorrect'])
                cn = int(coins1) + int(coins)
                ct = int(correct1) + int(correct)
                embed=discord.Embed(title="Playing HQ Offair Trivia...", description=f"**• Username : {username}\n• Games Played : 02\n• Questions Correct : {ct}/24\n• Coins Earned : {cn}\n• Total Coins : {tcoins}**", color=0x00ffff)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/773955381063974972.gif")
                await x.edit(embed=embed)
                break
        coins2 = int(coins)
        correct2 = int(correct)
        try:
            offair_id = api.start_offair()['gameUuid']
        except ApiResponseError:
            coins = int(coins1) + int(coins2)
            correct = int(correct1) + int(correct2)
            embed=discord.Embed(title="**Played Offair Trivia ✅**", description=f"**• Username : {username}\n• Games Played : 02\n• Questions Correct : {correct}/24\n• Coins Earned : {coins}\n• Total Coins : {tcoins}**", color=0x00ffff)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            await x.edit(embed=embed)
        while True:
            offair = api.offair_trivia(offair_id)
            answers = [unidecode(ans["text"]) for ans in offair['question']['answers']]
            question=offair['question']['question']
            option1=f"{answers[0]}"
            option2=f"{answers[1]}"
            option3=f"{answers[2]}"
            await asyncio.sleep(2)
            if question in q_list:
                option = q_base.find_one({'question': question})['option']
                select = int(option)
            else:
                select = int(2)
            data = api.send_offair_answer(offair_id, offair['question']['answers'][select - 1]['offairAnswerId'])
            #print(data)
            answer_counts = {}
            correct = ""
            for answer in data["answerCounts"]:
                ans_str = unidecode(answer["answer"])

                if answer["correct"]:
                    correct = ans_str
            coins = str(data["coinsEarned"])
            qcnt = (offair['question']['questionNumber'])
            qs = int(24) + int(qcnt)
            s = int(coins2) + int(coins1)
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
                coins = str(data['gameSummary']['coinsEarned'])
                correct = str(data['gameSummary']['questionsCorrect'])
                cn = int(coins1) + int(coins2) + int(coins)
                ct = int(correct1) + int(correct2) + int(correct)
                embed=discord.Embed(title="Playing HQ Offair Trivia...", description=f"**• Username : {username}\n• Games Played : 03\n• Questions Correct : {ct}/36\n• Coins Earned : {cn}\n• Total Coins : {tcoins}**", color=0x00ffff)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/773955381063974972.gif")
                await x.edit(embed=embed)
                break
        coins3 = int(coins)
        correct3 = int(correct)
        try:
            offair_id = api.start_offair()['gameUuid']
        except ApiResponseError:
            coins = int(coins1) + int(coins2) + int(coins3)
            correct = int(correct1) + int(correct2) + int(correct3)
            embed=discord.Embed(title="**Played Offair Trivia ✅**", description=f"**• Username : {username}\n• Games Played : 03\n• Questions Correct : {correct}/36\n• Coins Earned : {coins}\n• Total Coins : {tcoins}**", color=0x00ffff)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            await x.edit(embed=embed)
        while True:
            offair = api.offair_trivia(offair_id)
            answers = [unidecode(ans["text"]) for ans in offair['question']['answers']]
            question=offair['question']['question']
            option1=f"{answers[0]}"
            option2=f"{answers[1]}"
            option3=f"{answers[2]}"
            await asyncio.sleep(2)
            if question in q_list:
                option = q_base.find_one({'question': question})['option']
                select = int(option)
            else:
                select = int(2)
            data = api.send_offair_answer(offair_id, offair['question']['answers'][select - 1]['offairAnswerId'])
            #print(data)
            answer_counts = {}
            correct = ""
            for answer in data["answerCounts"]:
                ans_str = unidecode(answer["answer"])

                if answer["correct"]:
                    correct = ans_str
            coins = str(data["coinsEarned"])
            qcnt = (offair['question']['questionNumber'])
            qs = int(36) + int(qcnt)
            s = int(coins3) + int(coins2) +int(coins1)
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
                coins = str(data['gameSummary']['coinsEarned'])
                correct = str(data['gameSummary']['questionsCorrect'])
                cn = int(coins1) + int(coins2) + int(coins) + int(coins3)
                ct = int(correct1) + int(correct2) + int(correct) + int(correct3)
                embed=discord.Embed(title="Playing HQ Offair Trivia...", description=f"**• Username : {username}\n• Games Played : 04\n• Questions Correct : {ct}/48\n• Coins Earned : {cn}\n• Total Coins : {tcoins}**", color=0x00ffff)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/773955381063974972.gif")
                await x.edit(embed=embed)
                break
        coins4 = int(coins)
        correct4 = int(correct)
        try:
            offair_id = api.start_offair()['gameUuid']
        except ApiResponseError:
            coins = int(coins1) + int(coins2) + int(coins3) + int(coins4)
            correct = int(correct1) + int(correct2) + int(correct3) + int(correct4)
            embed=discord.Embed(title="**Played Offair Trivia ✅**", description=f"**• Username : {username}\n• Games Played : 04\n• Questions Correct : {correct}/48\n• Coins Earned : {coins}\n• Total Coins : {tcoins}**", color=0x00ffff)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            await x.edit(embed=embed)
        while True:
            offair = api.offair_trivia(offair_id)
            answers = [unidecode(ans["text"]) for ans in offair['question']['answers']]
            question=offair['question']['question']
            option1=f"{answers[0]}"
            option2=f"{answers[1]}"
            option3=f"{answers[2]}"
            await asyncio.sleep(2)
            if question in q_list:
                option = q_base.find_one({'question': question})['option']
                select = int(option)
            else:
                select = int(2)
            data = api.send_offair_answer(offair_id, offair['question']['answers'][select - 1]['offairAnswerId'])
            #print(data)
            answer_counts = {}
            correct = ""
            for answer in data["answerCounts"]:
                ans_str = unidecode(answer["answer"])

                if answer["correct"]:
                    correct = ans_str
            coins = str(data["coinsEarned"])
            qcnt = (offair['question']['questionNumber'])
            qs = int(48) + int(qcnt)
            s = int(coins3) + int(coins2) +int(coins1) + int(coins4)
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
                coins = str(data['gameSummary']['coinsEarned'])
                correct = str(data['gameSummary']['questionsCorrect'])
                coins = int(coins) + int(coins1) + int(coins2) + int(coins3) + int(coins)
                correct = int(correct) + int(correct1) + int(correct2) + int(correct3) + int(correct)
                embed=discord.Embed(title="**Played Offair Trivia ✅**", description=f"**• Username : {username}\n• Games Played : 05\n• Questions Correct : {correct}/60\n• Coins Earned : {coins}\n• Total Coins : {tcoins}**", color=0x00ffff)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                await x.edit(embed=embed)
                await asyncio.sleep(1)
                await x.edit(embed=embed)
                break


def setup(client):
    client.add_cog(DcPlay(client))
