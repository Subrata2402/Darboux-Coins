import sys
import traceback
import discord, aniso8601
from discord.ext import commands
from discord import app_commands
from HQApi import HQApi
from database import db
import bot_config

class Cashout(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="payout", description="Check your payout.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(username="Username of the account.")
    async def _payout(self, interaction: discord.Interaction, username: str):
        """Get recent payment details."""
        await interaction.response.defer()
        if interaction.guild:
            return await interaction.followup.send(bot_config.dm_message(interaction))
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
        username = data["username"]
        data = await api.get_payouts_me()
        description_info = ""
        for index, data in enumerate(data["payouts"]):
            if index+1 > 10: break
            amount = data["amount"]
            email = data["targetEmail"]
            tim = data["created"]
            tm = aniso8601.parse_datetime(tim).timestamp()
            create_at = f"<t:{int(tm)}>"
            tim = data["modified"]
            tm = aniso8601.parse_datetime(tim).timestamp()
            modify_at = f"<t:{int(tm)}>"
            description_info += f"• Amount :** {amount}**\n• Email :** {email}**\n• Payment Created :** {create_at}**\n• Payment Completed :** {modify_at}**\n\n"
        embed=discord.Embed(title=f"**__Payout Summary of {username} !__**", description=description_info, color=discord.Colour.random())
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
        embed.set_thumbnail(url=self.client.user.avatar.url)
        await interaction.followup.send(embed=embed)


    @app_commands.command(name="cashout", description="Cashout your earnings.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(username="Username of the account.", email="Email to which you want to cashout.")
    async def _cashout(self, interaction: discord.Interaction, username: str, email: str):
        """Cashout your earnings."""
        await interaction.response.defer()
        if interaction.guild:
            return await interaction.followup.send(bot_config.dm_message(interaction))
        check_if_exist = await db.profile_base.find_one({"id": interaction.user.id, "username": username.lower()})
        if not check_if_exist:
            return await interaction.followup.send(bot_config.account_not_found_message(username))
        api = HQApi(check_if_exist.get('access_token'))
        data = await api.get_payouts_me()
        if data.get("error"):
            if data["errorCode"] == 102:
                return await interaction.followup.send(bot_config.token_expired_message(username))
            else:
                return await interaction.followup.send(f"```\n{data['error']}\n```")
        bal = data["balance"]
        available = float(bal["available"][1:])
        if available < float(5):
            need = float(5) - available
            need_money = "{:.2f}".format(need)
            embed=discord.Embed(title="⚠️ Insufficient Balance", description=f"You don't have sufficient balance for cashout. You need more **${need_money}** for cashout.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar.url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
            return await interaction.followup.send(embed=embed)
        data = await api.make_payout(email)
        if data.get("error"):
            return await interaction.followup.send(f"```\n{data['error']}\n```")
        data = data["data"]
        amount = data["amount"]
        email = data["targetEmail"]
        embed=discord.Embed(title="Cashout Done ✅", description=f"Successfully Cashout of Amount **{amount}** to PayPal Email **{email}**", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar.url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
        await interaction.followup.send(embed=embed)
        channel = self.client.get_channel(bot_config.CASHOUT_CHANNEL_ID)
        await channel.send(f"**{interaction.user}** made a Successfully cashout of amount **{amount}**")

    @_cashout.error
    @_payout.error
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
    await client.add_cog(Cashout(client))
