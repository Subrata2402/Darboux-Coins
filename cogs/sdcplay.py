import discord, asyncio
from discord.ext import commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from database import db


class DcPlay(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(aliases=["splay"])
    async def sdcplay(self, ctx, username:str=None):
        """Play HQ Daily Challenge."""
        if username is None:
            embed=discord.Embed(title="⚠️ Invalid Argument", description=f"You didn't write username after `{ctx.prefix}dcplay`. Please correct use Command to play HQ Trivia Daily Challenge.\n`{ctx.prefix}dcplay <username>`\nExample: `{ctx.prefix}add +13158686534`", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        try:
            await ctx.message.delete()
        except:
            pass
        check_id = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()})
        if not check_id:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        try:
            api = HQApi(db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()}).get("access_token"))
            data = await api.get_users_me()
        except ApiResponseError:
            embed=discord.Embed(title="⚠️ Token Expired", description=f"This account token is expired. Please use Command `{ctx.prefix}refresh {username}` to refresh your account.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        coins = data["coins"]
        embed=discord.Embed(title="Starting HQ Offair Trivia...", color=0x00ffff)
        x = await ctx.send(embed=embed)
        if ctx.guild: username = "||Private Account||"
        await asyncio.sleep(2)
        embed=discord.Embed(title="Playing HQ Offair Trivia...", description=f"**• Username : {username}\n• Games Played : 00\n• Questions Correct : 00/00\n• Coins Earned : 0\n• Total Coins : {coins}**", color=discord.Colour.random())
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url=self.fetching_thumb)
        await x.edit(embed=embed)
        questions_list = [data.get("question") for data in list(db.questions_base.find())]
        try:
            offair_id = (await api.start_offair())['gameUuid']
        except ApiResponseError:
            offair_id = (await api.get_schedule())['offairTrivia']["waitTimeMs"]
            time=int(offair_id)/int(1000)
            hours, remainder = divmod(time, 3600)
            minutes, seconds = divmod(remainder, 60)
            hours, minutes, seconds = int(hours), int(minutes), int(seconds)
            await asyncio.sleep(1)
            if hours + minutes == 0:
                embed=discord.Embed(description=f"You have played all games as of now, so you must wait **{seconds}** second{'' if seconds == 1 else 's'} to play Daily Challenge once again.", color=discord.Colour.random())
                await x.edit(embed=embed)
            elif hours == 0:
                embed=discord.Embed(description=f"You have played all games as of now, so you must wait **{minutes}** minute{'' if minutes == 1 else 's'} **{seconds}** second{'' if seconds == 1 else 's'} to play Daily Challenge once again.", color=discord.Colour.random())
                await x.edit(embed=embed)
            elif minutes == 0:
                embed=discord.Embed(description=f"You have played all games as of now, so you must wait **{hours}** hour{'' if hours == 1 else 's'} and **{seconds}** second{'' if seconds == 1 else 's'} to play Daily Challenge once again.", color=discord.Colour.random())
                await x.edit(embed=embed)
            else:
                embed=discord.Embed(description=f"You have played all games as of now, so you must wait **{hours}** hour{'' if hours == 1 else 's'} **{minutes}** minute{'' if minutes == 1 else 's'} and **{seconds}** second{'' if seconds == 1 else 's'} to play Daily Challenge once again.", color=discord.Colour.random())
                await x.edit(embed=embed)
            if time == 0:
                offair_id = (await api.get_schedule())['offairTrivia']['games'][0]['gameUuid']
            else:
                return
        while True:
            offair = await api.offair_trivia(offair_id)
            answers = [unidecode(ans["text"]) for ans in offair['question']['answers']]
            question=offair['question']['question']
            option1=answers[0]
            option2=answers[1]
            option3=answers[2]
            await asyncio.sleep(2)
            answer = await self.get_answer(question)
            if answer:
                if option1.lower() == answer.lower(): select = 1
                elif option2.lower() == answer.lower(): select = 2
                else: select = 3
            else: select = 2
            data = await api.send_offair_answer(offair_id, offair['question']['answers'][select - 1]['offairAnswerId'])
            for answer in data["answerCounts"]:
                if answer["correct"]: correct = unidecode(answer["answer"])
            await self.add_question(question, correct)
            coins = str(data["coinsEarned"])
            qcnt = (offair['question']['questionNumber'])
            qs = int(0) + int(qcnt)
            
            if data['gameSummary']:
                tcoins = str(data['gameSummary']['coinsTotal'])
                coins = str(data['gameSummary']['coinsEarned'])
                correct = str(data['gameSummary']['questionsCorrect'])
                embed=discord.Embed(title="Playing HQ Offair Trivia...", description=f"**• Username : {username}\n• Games Played : 01\n• Questions Correct : {correct}/12\n• Coins Earned : {coins}\n• Total Coins : {tcoins}**", color=discord.Colour.random())
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/773955381063974972.gif")
                await x.edit(embed=embed)
                break
        coins1 = int(coins)
        correct1 = int(correct)
        try:
            offair_id = (await api.start_offair())['gameUuid']
        except ApiResponseError:
            embed=discord.Embed(title="**Played Offair Trivia ✅**", description=f"**• Username : {username}\n• Games Played : 01\n• Questions Correct : {correct1}/12\n• Coins Earned : {coins1}\n• Total Coins : {tcoins}**", color=discord.Colour.random())
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            return await x.edit(embed=embed)
        while True:
            offair = await api.offair_trivia(offair_id)
            answers = [unidecode(ans["text"]) for ans in offair['question']['answers']]
            question=offair['question']['question']
            option1=f"{answers[0]}"
            option2=f"{answers[1]}"
            option3=f"{answers[2]}"
            await asyncio.sleep(2)
            answer = await self.get_answer(question)
            if answer:
                if option1.lower() == answer.lower(): select = 1
                elif option2.lower() == answer.lower(): select = 2
                else: select = 3
            else: select = 2
            data = await api.send_offair_answer(offair_id, offair['question']['answers'][select - 1]['offairAnswerId'])
            for answer in data["answerCounts"]:
                if answer["correct"]: correct = unidecode(answer["answer"])
            await self.add_question(question, correct)
            coins = str(data["coinsEarned"])
            qcnt = (offair['question']['questionNumber'])
            qs = int(12) + int(qcnt)
            s = coins1
            if data['gameSummary']:
                tcoins = str(data['gameSummary']['coinsTotal'])
                coins = str(data['gameSummary']['coinsEarned'])
                correct = str(data['gameSummary']['questionsCorrect'])
                cn = int(coins1) + int(coins)
                ct = int(correct1) + int(correct)
                embed=discord.Embed(title="Playing HQ Offair Trivia...", description=f"**• Username : {username}\n• Games Played : 02\n• Questions Correct : {ct}/24\n• Coins Earned : {cn}\n• Total Coins : {tcoins}**", color=discord.Colour.random())
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/773955381063974972.gif")
                await x.edit(embed=embed)
                break
        coins2 = int(coins)
        correct2 = int(correct)
        try:
            offair_id = (await api.start_offair())['gameUuid']
        except ApiResponseError:
            coins = int(coins1) + int(coins2)
            correct = int(correct1) + int(correct2)
            embed=discord.Embed(title="**Played Offair Trivia ✅**", description=f"**• Username : {username}\n• Games Played : 02\n• Questions Correct : {correct}/24\n• Coins Earned : {coins}\n• Total Coins : {tcoins}**", color=discord.Colour.random())
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            return await x.edit(embed=embed)
        while True:
            offair = await api.offair_trivia(offair_id)
            answers = [unidecode(ans["text"]) for ans in offair['question']['answers']]
            question=offair['question']['question']
            option1=f"{answers[0]}"
            option2=f"{answers[1]}"
            option3=f"{answers[2]}"
            await asyncio.sleep()
            answer = await self.get_answer(question)
            if answer:
                if option1.lower() == answer.lower(): select = 1
                elif option2.lower() == answer.lower(): select = 2
                else: select = 3
            else: select = 2
            data = await api.send_offair_answer(offair_id, offair['question']['answers'][select - 1]['offairAnswerId'])
            for answer in data["answerCounts"]:
                if answer["correct"]: correct = unidecode(answer["answer"])
            await self.add_question(question, correct)
            coins = str(data["coinsEarned"])
            qcnt = (offair['question']['questionNumber'])
            qs = int(24) + int(qcnt)
            s = int(coins2) + int(coins1)
            
            if data['gameSummary']:
                tcoins = str(data['gameSummary']['coinsTotal'])
                coins = str(data['gameSummary']['coinsEarned'])
                correct = str(data['gameSummary']['questionsCorrect'])
                cn = int(coins1) + int(coins2) + int(coins)
                ct = int(correct1) + int(correct2) + int(correct)
                embed=discord.Embed(title="Playing HQ Offair Trivia...", description=f"**• Username : {username}\n• Games Played : 03\n• Questions Correct : {ct}/36\n• Coins Earned : {cn}\n• Total Coins : {tcoins}**", color=discord.Colour.random())
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/773955381063974972.gif")
                await x.edit(embed=embed)
                break
        coins3 = int(coins)
        correct3 = int(correct)
        try:
            offair_id = (await api.start_offair())['gameUuid']
        except ApiResponseError:
            coins = int(coins1) + int(coins2) + int(coins3)
            correct = int(correct1) + int(correct2) + int(correct3)
            embed=discord.Embed(title="**Played Offair Trivia ✅**", description=f"**• Username : {username}\n• Games Played : 03\n• Questions Correct : {correct}/36\n• Coins Earned : {coins}\n• Total Coins : {tcoins}**", color=discord.Colour.random())
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            return await x.edit(embed=embed)
        while True:
            offair = await api.offair_trivia(offair_id)
            answers = [unidecode(ans["text"]) for ans in offair['question']['answers']]
            question=offair['question']['question']
            option1=f"{answers[0]}"
            option2=f"{answers[1]}"
            option3=f"{answers[2]}"
            await asyncio.sleep(2)
            answer = await self.get_answer(question)
            if answer:
                if option1.lower() == answer.lower(): select = 1
                elif option2.lower() == answer.lower(): select = 2
                else: select = 3
            else: select = 2
            data = await api.send_offair_answer(offair_id, offair['question']['answers'][select - 1]['offairAnswerId'])
            for answer in data["answerCounts"]:
                if answer["correct"]: correct = unidecode(answer["answer"])
            await self.add_question(question, correct)
            coins = str(data["coinsEarned"])
            qcnt = (offair['question']['questionNumber'])
            qs = int(36) + int(qcnt)
            s = int(coins3) + int(coins2) +int(coins1)
            
            if data['gameSummary']:
                tcoins = str(data['gameSummary']['coinsTotal'])
                coins = str(data['gameSummary']['coinsEarned'])
                correct = str(data['gameSummary']['questionsCorrect'])
                cn = int(coins1) + int(coins2) + int(coins) + int(coins3)
                ct = int(correct1) + int(correct2) + int(correct) + int(correct3)
                embed=discord.Embed(title="Playing HQ Offair Trivia...", description=f"**• Username : {username}\n• Games Played : 04\n• Questions Correct : {ct}/48\n• Coins Earned : {cn}\n• Total Coins : {tcoins}**", color=discord.Colour.random())
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/773955381063974972.gif")
                await x.edit(embed=embed)
                break
        coins4 = int(coins)
        correct4 = int(correct)
        try:
            offair_id = (await api.start_offair())['gameUuid']
        except ApiResponseError:
            coins = int(coins1) + int(coins2) + int(coins3) + int(coins4)
            correct = int(correct1) + int(correct2) + int(correct3) + int(correct4)
            embed=discord.Embed(title="**Played Offair Trivia ✅**", description=f"**• Username : {username}\n• Games Played : 04\n• Questions Correct : {correct}/48\n• Coins Earned : {coins}\n• Total Coins : {tcoins}**", color=discord.Colour.random())
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            return await x.edit(embed=embed)
        while True:
            offair = await api.offair_trivia(offair_id)
            answers = [unidecode(ans["text"]) for ans in offair['question']['answers']]
            question=offair['question']['question']
            option1=f"{answers[0]}"
            option2=f"{answers[1]}"
            option3=f"{answers[2]}"
            await asyncio.sleep(2)
            answer = await self.get_answer(question)
            if answer:
                if option1.lower() == answer.lower(): select = 1
                elif option2.lower() == answer.lower(): select = 2
                else: select = 3
            else: select = 2
            data = await api.send_offair_answer(offair_id, offair['question']['answers'][select - 1]['offairAnswerId'])
            for answer in data["answerCounts"]:
                if answer["correct"]: correct = unidecode(answer["answer"])
            await self.add_question(question, correct)
            coins = str(data["coinsEarned"])
            qcnt = (offair['question']['questionNumber'])
            qs = int(48) + int(qcnt)
            s = int(coins3) + int(coins2) +int(coins1) + int(coins4)
            
            if data['gameSummary']:
                tcoins = str(data['gameSummary']['coinsTotal'])
                coins = str(data['gameSummary']['coinsEarned'])
                correct = str(data['gameSummary']['questionsCorrect'])
                coins = int(coins) + int(coins1) + int(coins2) + int(coins3) + int(coins)
                correct = int(correct) + int(correct1) + int(correct2) + int(correct3) + int(correct)
                embed=discord.Embed(title="**Played Offair Trivia ✅**", description=f"**• Username : {username}\n• Games Played : 05\n• Questions Correct : {correct}/60\n• Coins Earned : {coins}\n• Total Coins : {tcoins}**", color=discord.Colour.random())
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                await x.edit(embed=embed)
                await asyncio.sleep(1)
                await x.edit(embed=embed)
                break

def setup(client):
    client.add_cog(DcPlay(client))
