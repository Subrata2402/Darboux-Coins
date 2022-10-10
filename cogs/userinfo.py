import sys
import traceback
import discord, aniso8601
from discord.ext import commands
from discord import app_commands
from HQApi import HQApi


class UserStats(commands.Cog, HQApi):

    def __init__(self, client: commands.Bot):
        super().__init__()
        self.client = client

    @app_commands.command(name="hquser", description="Get HQ trivia stats of a user.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(username="Username of the user.")
    async def _hq_user_stats(self, interaction: discord.Interaction, username: str):
        """Get HQ trivia stats of a user."""
        await interaction.response.defer()
        login_token = "KwmTCpQzIqiLLlxDsK7cf8mIvETtYdyofrBr4R7x6py1aH57pokb6XHdEXRcSeGk"
        api = HQApi((await self.get_tokens(login_token))["accessToken"])
        data = await api.search(username)
        if not data["data"]:
            return await interaction.followup.send(f"Couldn't find any HQ account account with name `{username}`.")
        id = data["data"][0]["userId"]
        data = await api.get_user(id)
        username = data["username"]
        id = data["userId"]
        avatar_url = data["avatarUrl"]
        create_at = data["created"]
        tm = aniso8601.parse_datetime(create_at).timestamp()
        total = data["leaderboard"]["total"]
        unclaimed = data["leaderboard"]["unclaimed"]
        winCount = data["winCount"]
        gamesPlayed = data["gamesPlayed"]
        highScore = data["highScore"]
        refferal = data["referralUrl"]
        embed=discord.Embed(title=f"HQ User Stats", color=discord.Colour.random())
        embed.add_field(name="Username", value=username)
        embed.add_field(name="User ID", value=id)
        embed.add_field(name="Created On", value=f"<t:{int(tm)}>")
        embed.add_field(name="Total Winnings", value=f"{total} (Unclaimed : {unclaimed})")
        embed.add_field(name="High Score", value=highScore)
        embed.add_field(name="Games Won", value=f"{winCount}/{gamesPlayed}")
        embed.add_field(name="Refferal Url", value=f"[Click Here]({refferal})")
        embed.set_thumbnail(url=avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
        await interaction.followup.send(embed=embed)

    @_hq_user_stats.error
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
    await client.add_cog(UserStats(client))