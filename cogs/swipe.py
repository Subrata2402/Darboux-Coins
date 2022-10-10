import sys
import traceback
import discord, asyncio
from discord.ext import commands
from discord import app_commands
from HQApi import HQApi
from database import db
import bot_config

class Swipe(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="swipe", description="Swipe to earn an extra life.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(username="Username of the account.")
    async def _swipe(self, interaction: discord.Interaction, username: str):
        """Swipe and earn extra life."""
        await interaction.response.defer()
        check_if_exist = await db.profile_base.find_one({"id": interaction.user.id, "username": username.lower()})
        if not check_if_exist:
            return await interaction.followup.send(bot_config.account_not_found_message(username))
        api = HQApi(check_if_exist.get("access_token"))
        data = await api.get_users_me()
        if data.get("error"):
            if data["errorCode"] == 102:
                return await interaction.followup.send(bot_config.token_expired_message(username))
            else:
                return await interaction.followup.send(f"```\n{data['error']}\n```")
        data = await api.swipe()
        if data.get("error"):
            embed=discord.Embed(title="⚠️ Swiped Failed", description=f"You have already swiped your account in this month.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
            return await interaction.followup.send(embed=embed)
        data = data["data"]
        embed=discord.Embed(title="Swiped Done ✅", description=f"You have successfully swiped your account and earn an Extra <:extra_life:844448511264948225> Life.", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
        await interaction.followup.send(embed=embed)

    @_swipe.error
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
    await client.add_cog(Swipe(client))
