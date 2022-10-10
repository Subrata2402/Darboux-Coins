import sys
import traceback
from typing import Literal
import discord, asyncio
from discord.ext import commands
from discord import app_commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from database import db
from unidecode import unidecode
import bot_config

class AutoPlay(commands.Cog, HQApi):
    
    def __init__(self, client: commands.Bot):
        super().__init__()
        self.client = client

    async def get_answer(self, question) -> str:
        check_question = await db.questions_base.find_one({"question": question.lower()})
        if not check_question: return None
        answer = check_question.get("answer")
        return answer

    async def add_question(self, question, answer) -> None:
        check_question = await db.questions_base.find_one({"question": question.lower()})
        if not check_question:
            await db.questions_base.insert_one({"question": question.lower(), "answer": answer.lower()})

    async def auto_play(self) -> None:
        for all_data in [data async for data in db.profile_base.find({"auto_play": True})]:
            await asyncio.sleep(30)
            active = (await self.get_show())["active"]
            if active:
                await asyncio.sleep(600)
                continue
            api = HQApi(all_data.get("access_token"))
            data = await api.get_users_me()
            if data.get("error"):
                if data["errorCode"] == 102:
                    try:
                        update = {"auto_play": False}
                        await db.profile_base.update_one({"id": all_data.get("id"), "user_id": all_data.get("user_id")}, {"$inc": update})
                        embed = discord.Embed(title = "⚠️ Token Expired",
                            description = f"{all_data.get('username')}'s token has expired! For that I can't play your daily challenge, please refresh your account by `/refresh {all_data.get('username')}` and after refresh your account please on auto play mode once again.",
                            color = discord.Colour.random())
                        user = self.client.get_user(all_data.get("id"))
                        await user.send(content = user.mention, embed = embed)
                    except Exception as e:
                        print(e)
                continue
            coins = data["coins"]
            if coins >= 1500: continue
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
                member = self.client.get_user(all_data.get("id"))
                if data['gameSummary']:
                    tcoins = str(data['gameSummary']['coinsTotal'])
                    coins = str(data['gameSummary']['coinsEarned'])
                    correct = str(data['gameSummary']['questionsCorrect'])
                    embed=discord.Embed(title="Played HQ Offair Trivia ✅", description=f"**• Username : ||Private Account||\n• Games Played : 01\n• Questions Correct : {correct}/12\n• Coins Earned : {coins}\n• Total Coins : {tcoins}**", color=discord.Colour.random())
                    embed.set_footer(text=member, icon_url=member.avatar_url)
                    embed.set_thumbnail(url=self.client.user.avatar_url)
                    channel = self.client.get_channel(957198388028375050)
                    await channel.send(embed = embed)
                    break

        await asyncio.sleep(60)
        await self.auto_play()
                    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.auto_play()
                
    @app_commands.command(name="autoplay", description="Enable or disable auto play mode.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(username="Username of your account.", mode="Enable or disable auto play mode.")
    async def _auto_play(self, interaction: discord.Interaction, username: str, mode: Literal["enable", "disable"]):
        await interaction.response.defer()
        check_if_exist = await db.profile_base.find_one({"id": interaction.user.id, "username": username.lower()})
        if not check_if_exist:
            return await interaction.followup.send(bot_config.account_not_found_message(username))
        if mode.lower() == "enable":
            mode = (await db.profile_base.find_one({"id": interaction.user.id, "username": username.lower()})).get("auto_play")
            if not mode:
                update = {"auto_play": True}
                await db.profile_base.update_one({"id": interaction.user.id, "username": username.lower()}, {"$inc": update})
                embed = discord.Embed(title = "Enabled Auto Play Mode ✅", description = f"You have successfully enabled auto play mode for `{username}`", color = discord.Colour.random())
                return await interaction.followup.send(embed = embed)
            embed = discord.Embed(title = "⚠️ Already Enabled Auto Play Mode", description = f"Auto play mode already enabled for `{username}`", color = discord.Colour.random())
            await interaction.followup.send(embed = embed)
        elif mode.lower() == "disable":
            mode = (await db.profile_base.find_one({"id": interaction.user.id, "username": username.lower()})).get("auto_play")
            if mode:
                update = {"auto_play": False}
                await db.profile_base.update_one({"id": interaction.user.id, "username": username.lower()}, {"$inc": update})
                embed = discord.Embed(title = "Disabled Auto Play Mode ✅", description = f"You have successfully disabled auto play mode for `{username}`", color = discord.Colour.random())
                return await interaction.followup.send(embed = embed)
            embed = discord.Embed(title = "⚠️ Already Disabled Auto Play Mode", description = f"Auto play mode already disabled for `{username}`", color = discord.Colour.random())
            await interaction.followup.send(embed = embed)


    @_auto_play.error
    async def _app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """Error handler for app commands"""
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"This command is on cooldown. Try again in **{round(error.retry_after, 2)}** seconds.", ephemeral=True)
        elif isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("The command execution is failed for some conditions are not satisfied. ", ephemeral=True)
        else:
            print(f"Error loading {interaction.command} command!", file=sys.stderr)
            traceback.print_exc()


async def setup(client: commands.Bot):
    await client.add_cog(AutoPlay(client))