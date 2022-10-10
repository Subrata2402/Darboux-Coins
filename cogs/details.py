import discord, aniso8601
from discord.ext import commands
from discord import app_commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError, NotAuthenticatedError
from database import db
import bot_config

class Details(commands.Cog):

    def __init__(self, client):
        self.client = client

    @app_commands.command(name="details", description="Get account details.")
    @app_commands.describe(username="Username of the account.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def _details(self, interaction: discord.Interaction, username: str):
        await interaction.response.defer()
        if interaction.guild:
            return interaction.followup.send(bot_config.dm_message(interaction))
        data = await db.profile_base.find_one({"id": interaction.user.id, "username": username.lower()})
        if not data:
            return await interaction.followup.send(bot_config.account_not_found_message(username))
        try:
            api = HQApi(data["access_token"])
            user_data = await api.get_users_me()
            if user_data.get("error"):
                if user_data["errorCode"] == 102:
                    return await interaction.followup.send(bot_config.token_expired_message(username))
                else:
                    return await interaction.followup.send(f"```\n{user_data['error']}\n```")
        except Exception as error:
            return await interaction.followup.send(f"```\n{error}\n```")
        coins = user_data.get("coins") if user_data.get("coins") else 0
        payout_data = await api.get_payouts_me()
        balance_data = payout_data['balance']
        # unclaimed = balance_data['frozen']
        auto_play_mode = data["auto_play"]
        embed = discord.Embed(title = f"**__Statistics of HQ Account !__**",
            description = f"**• Username :** {user_data['username']}\n" \
                f"**• Mobile Number :** {user_data['phoneNumber']}\n" \
                f"**• Auto-play Mode :** {'Enable' if auto_play_mode else 'Disable'}\n"
                f"**• Blocked :** {user_data['blocksMe']}",
            color = discord.Colour.random())
        embed.add_field(name = f"🔥 __PowerUps Details :__-", inline = False,
            value = f"**• Total Coins :** {coins} {bot_config.emoji.exatra_coins}\n" \
                f"**• Total Lives :** {user_data['items']['lives']} {bot_config.emoji.extra_life}\n" \
                f"**• Super Spins :** {user_data['items']['superSpins']} {bot_config.emoji.super_spin}\n" \
                f"**• Total Erasers :** {user_data['items']['erase1s']} {bot_config.emoji.erasers}\n" \
            )
        embed.add_field(name = "💸 __Balance & Cashout Details :__-", inline = False,
            value = f"**• Total Balance :** {balance_data['prizeTotal']}\n" \
                f"**• Claimed Ammount :** {balance_data['paid']}\n" \
                f"**• Pending Ammount :** {balance_data['pending']}\n" \
                f"**• Unclaimed Ammount :** {balance_data['unpaid']}\n" \
                f"**• Available for Cashout :** {balance_data['available']}"
            )
        embed.add_field(name = "🔴 __Live Games Details :__-", inline = False,
            value = f"**• Games Won :** {user_data['leaderboard']['wins']}/{user_data['gamesPlayed']}\n" \
                f"**• High Score :** {user_data['highScore']}\n" \
                f"**• Rank :** {'None' if user_data['leaderboard']['rank'] == 101 else user_data['leaderboard']['rank']}\n"
            )
        embed.set_footer(text = f"ID: {user_data['userId']} | Created At")
        embed.timestamp = aniso8601.parse_datetime(user_data['created'])
        embed.set_thumbnail(url = user_data['avatarUrl'])
        await interaction.followup.send(embed = embed)

    @_details.error
    async def _app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """Error handler for app commands"""
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"This command is on cooldown. Try again in **{round(error.retry_after, 2)}** seconds.", ephemeral=True)
        elif isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("The command execution is failed for some conditions are not satisfied. ", ephemeral=True)


async def setup(client: commands.Bot):
    await client.add_cog(Details(client))