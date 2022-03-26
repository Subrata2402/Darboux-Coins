import discord, asyncio
from discord.ext import commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from database import db
from unidecode import unidecode

class AutoPlay(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    async def get_answer(self, question):
        check_question = db.questions_base.find_one({"question": question})
        if not check_question: return None
        answer = db.questions_base.find_one({"question": question}).get("answer")
        return answer

    async def add_question(self, question, answer):
        check_question = db.questions_base.find_one({"question": question})
        if not check_question:
            db.questions_base.insert_one({"question": question, "answer": answer})

    async def auto_play(self):
        for data in list(db.profile_base.find()):
            auto_play_mode = data.get('auto_play')
            if auto_play_mode:
                api = HQApi(data.get("access_token"))
                try:
                    data = await api.get_users_me()
                    username = data["username"]
                    coins = data["coins"]
                    if coins >= 1200: continue
                except:
                    try:
                        update = {"auto_play": False}
                        db.profile_base.update_one({"id": data.get("id"), "user_id": data.get("user_id")}, {"$set", update})
                        user = await self.client.get_user(data.get("id"))
                        embed = discord.Embed(title = "⚠️ Token Expired",
                            description = f"{data.get('username')}'s token has expired! For this I can't play your daily challenge, please refresh your account by `-refresh {data.get('username')}` and after refresh your account please on auto play mode once again.",
                            color = discord.Colour.random())
                        await user.send(content = user.mention, embed = embed)
                    except:
                        pass
                try:
                    offair_id = (await api.start_offair())['gameUuid']
                except ApiResponseError:
                    offair_id = (await api.get_schedule())['offairTrivia']["waitTimeMs"]
                    time=int(offair_id)/int(1000)
                    if time == 0:
                        offair_id = (await api.get_schedule())['offairTrivia']['games'][0]['gameUuid']
                    else:
                        continue
                while True:
                    offair = await api.offair_trivia(offair_id)
                    question = offair['question']['question']
                    db_answer = await self.get_answer(question)
                    select = 1
                    if db_answer:
                        for index, answer in enumerate(offair['question']['answers']):
                            if answer["text"].lower() == db_answer.lower():
                                select = index
                    data = await api.send_offair_answer(offair_id, offair['question']['answers'][select]['offairAnswerId'])
                    for answer in data["answerCounts"]:
                        if answer["correct"]: correct = unidecode(answer["answer"])
                    await self.add_question(question, correct)
                    if answer['gameSummary']:
                        tcoins = str(data['gameSummary']['coinsTotal'])
                        coins = str(data['gameSummary']['coinsEarned'])
                        correct = str(data['gameSummary']['questionsCorrect'])
                        embed=discord.Embed(title="Playing HQ Offair Trivia...", description=f"**• Username : {username}\n• Games Played : 01\n• Questions Correct : {correct}/12\n• Coins Earned : {coins}\n• Total Coins : {tcoins}**", color=discord.Colour.random())
                        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/773955381063974972.gif")
                        channel = self.client.get_channel(957198388028375050)
                        await channel.send(embed = embed)
                        break
        await asyncio.sleep(60)
        await self.auto_play()
                    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.auto_play()
                
    @commands.command()
    async def autoplay(self, ctx, username = None, mode = None):
        if not username: return await ctx.send(ctx.author.mention + " You didn't mention username.")
        if not mode: return await ctx.send(ctx.author.mention + " You didn't mention any mode. Please choose either `on` or `off` to set AutoPlay mode.")
        check_if_exist = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()})
        if not check_if_exist:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all saved accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        if mode.lower() == "on":
            mode = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()}).get("auto_play")
            if not mode:
                update = {"auto_play": True}
                db.profile_base.update_one({"id": ctx.author.id, "username": username.lower()}, {"$set": update})
                embed = discord.Embed(title = "Enabled Auto Play Mode ✅", description = f"You have successfully enabled auto play mode for `{username}`", color = discord.Colour.random())
                return await ctx.send(embed = embed)
            embed = discord.Embed(title = "⚠️ Already Enabled Auto Play Mode", description = f"Auto play mode already enabled for `{username}`", color = discord.Colour.random())
            await ctx.send(embed = embed)
        elif mode.lower() == "off":
            mode = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()}).get("auto_play")
            if mode:
                update = {"auto_play": False}
                db.profile_base.update_one({"id": ctx.author.id, "username": username.lower()}, {"$set": update})
                embed = discord.Embed(title = "Disabled Auto Play Mode ✅", description = f"You have successfully disabled auto play mode for `{username}`", color = discord.Colour.random())
                return await ctx.send(embed = embed)
            embed = discord.Embed(title = "⚠️ Already Disabled Auto Play Mode", description = f"Auto play mode already disabled for `{username}`", color = discord.Colour.random())
            await ctx.send(embed = embed)


def setup(client):
    client.add_cog(AutoPlay(client))