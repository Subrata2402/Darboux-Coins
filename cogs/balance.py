import sys
import traceback
import discord
from discord.ext import commands
from discord import app_commands
from HQApi import HQApi
from database import db
import bot_config

class Balance(commands.Cog, HQApi):

    def __init__(self, client: commands.Bot):
        super().__init__()
        self.client = client

    @app_commands.command(name="balance", description="Check your balance.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(username="Username of the account.")
    async def _balance(self, interaction: discord.Interaction, username: str):
        """Check your balance."""
        await interaction.response.defer()
        if interaction.guild:
            return await interaction.followup.send(bot_config.dm_message(interaction))
        check_id = await db.profile_base.find_one({"id": interaction.user.id})
        if not check_id:
            return await interaction.followup.send(bot_config.account_not_found_message(username))
        api = HQApi(check_id.get("access_token"))
        data = await api.get_payouts_me()
        if data.get("error"):
            if data["errorCode"] == 102:
                return await interaction.followup.send(bot_config.token_expired_message(username))
            else:
                return await interaction.followup.send(f"```\n{data['error']}\n```")
        bal = data["balance"]
        total = float(bal["prizeTotal"][1:])
        paid = float(bal["paid"][1:])
        pending = float(bal["pending"][1:])
        unpaid = float(bal["unpaid"][1:])
        available = float(bal["available"][1:])
        embed=discord.Embed(title=f"__Balance & Cashout Details of {username} :__-", description=f"**• Total Balance :** ${total} 💰\n**• Claimed Ammount :** ${paid} 💸\n**• Pending Ammount :** ${pending} 💰\n**• Unclaimed Ammount :** ${unpaid} 💸\n**• Available for Cashout :** ${available} 💰", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar.url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
        await interaction.followup.send(embed=embed)


    @_balance.error
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
    await client.add_cog(Balance(client))


