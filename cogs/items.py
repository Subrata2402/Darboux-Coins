import sys
import traceback
from typing import Literal
import discord
from discord.ext import commands
from discord import app_commands
from HQApi import HQApi
from database import db
import bot_config

class Items(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="life", description="Purchase an Extra Life to continue playing and get a chance to win a prize..")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(username="Username of the account.", amount="Amount of life to purchase.")
    async def _extra_life(self, interaction: discord.Interaction, username: str, amount: Literal[1, 3, 5]):
        """Purchase Extra Life."""
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
        coins = data["coins"]
        erasers = data["items"]["erase1s"]
        superSpins = data["items"]["superSpins"]
        if amount == 1:
            if coins < 400:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient <:extra_coins:844448578881847326> Coins to purchase an Extra <:extra_life:844448511264948225> Life. Play HQ Daily Challenge and earn some <:extra_coins:844448578881847326> Coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar.url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
                return await interaction.followup.send(embed=embed)
        elif amount == 3:
            if coins < 1000:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient <:extra_coins:844448578881847326> Coins to purchase 3 Extra <:extra_life:844448511264948225> Lifes. Play HQ Daily Challenge and earn some <:extra_coins:844448578881847326> Coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar.url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
                return await interaction.followup.send(embed=embed)
        elif amount == 5:
            if coins < 1500:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient <:extra_coins:844448578881847326> Coins to purchase 5 Extra <:extra_life:844448511264948225> Lifes. Play HQ Daily Challenge and earn some <:extra_coins:844448578881847326> Coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar.url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
                return await interaction.followup.send(embed=embed)
        data = await api.purchase_life(amount)
        coins = data["coinsTotal"]
        life = data["itemsTotal"]["extra-life"]
        embed=discord.Embed(title="Life Purchased ✅", description=f"You have successfully purchased {amount} Extra <:extra_life:844448511264948225> Life{'' if amount == 1 else 's'}!\n\n**• Total Coins :** {coins} <:extra_coins:844448578881847326>\n**• Total Lives :** {life} <:extra_life:844448511264948225>\n**• Total Erasers :** {erasers} <:eraser:844448550498205736>\n**• Total Super-spins :** {superSpins} <:super_spin:844448472908300299>", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar.url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="eraser", description="Purchase an Eraser to remove a wrong answer from a question.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(username="Username of the account.", amount="Amount of eraser to purchase.")
    async def _eraser(self, interaction: discord.Interaction, username: str, amount: Literal[1, 3, 5]):
        """Purchase Eraser."""
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
        coins = data["coins"]
        life = data["items"]["lives"]
        superSpins = data["items"]["superSpins"]
        if amount == 1:
            if coins < 100:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient <:extra_coins:844448578881847326> Coins to purchase an <:eraser:844448550498205736> Extra Eraser. Play HQ Daily Challenge and earn some <:extra_coins:844448578881847326> Coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar.url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
                return await interaction.followup.send(embed=embed)
        elif amount == 3:
            if coins < 250:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient <:extra_coins:844448578881847326> Coins to purchase 3 <:eraser:844448550498205736> Extra Erasers. Play HQ Daily Challenge and earn some <:extra_coins:844448578881847326> Coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar.url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
                return await interaction.followup.send(embed=embed)
        elif amount == 5:
            if coins < 400:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient <:extra_coins:844448578881847326> Coins to purchase 5 <:eraser:844448550498205736> Extra Erasers. Play HQ Daily Challenge and earn some <:extra_coins:844448578881847326> Coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar.url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
                return await interaction.followup.send(embed=embed)
        data = await api.purchase_eraser(amount)
        coins = data["coinsTotal"]
        erasers = data["itemsTotal"]["eraser"]
        embed=discord.Embed(title="Eraser Purchased ✅", description=f"You have successfully purchased {amount} <:eraser:844448550498205736> Extra Eraser{'' if amount == 1 else 's'}!\n\n**• Total Coins :** {coins} <:extra_coins:844448578881847326>\n**• Total Lives :** {life} <:extra_life:844448511264948225>\n**• Total Erasers :** {erasers} <:eraser:844448550498205736>\n**• Total Super-spins :** {superSpins} <:super_spin:844448472908300299>", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar.url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="super-spin", description="Purchase a Super Spin to get a chance to win a prize.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(username="Username of the account.", amount="Amount of eraser to purchase.")
    async def _super_spin(self, interaction: discord.Interaction, username: str, amount: Literal[1, 3, 5]):
        """Purchase superspin."""
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
        coins = data["coins"]
        erasers = data["items"]["erase1s"]
        life = data["items"]["lives"]
        superSpins = data["items"]["superSpins"]
        if amount == 1:
            if coins < 150:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient <:extra_coins:844448578881847326> Coins to purchase an Extra <:super_spin:844448472908300299> Super-spin. Play HQ Daily Challenge and earn some <:extra_coins:844448578881847326> Coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar.url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
                return await interaction.followup.send(embed=embed)
        elif amount == 3:
            if coins < 400:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient <:extra_coins:844448578881847326> Coins to purchase 3 Extra <:super_spin:844448472908300299> Super-spins. Play HQ Daily Challenge and earn some <:extra_coins:844448578881847326> Coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar.url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
                return await interaction.followup.send(embed=embed)
        elif amount == 5:
            if coins < 600:
                embed=discord.Embed(title="⚠️ Api Response Error", description=f"You don't have sufficient <:extra_coins:844448578881847326> Coins to purchase 5 Extra <:super_spin:844448472908300299> Super-spins. Play HQ Daily Challenge and earn some <:extra_coins:844448578881847326> Coins!", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar.url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
                return await interaction.followup.send(embed=embed)
        data = await api.purchase_super_spin(amount)
        coins = data["coinsTotal"]
        superSpins = int(superSpins) + int(amount)
        embed=discord.Embed(title="Super-spin Purchased ✅", description=f"You have successfully purchased {amount} Extra <:super_spin:844448472908300299> Super-spin{'' if amount == 1 else 's'}!\n\n**• Total Coins :** {coins} <:extra_coins:844448578881847326>\n**• Total Lives :** {life} <:extra_life:844448511264948225>\n**• Total Erasers :** {erasers} <:eraser:844448550498205736>\n**• Total Super-spins :** {superSpins} <:super_spin:844448472908300299>", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar.url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
        await interaction.followup.send(embed=embed)


    @_super_spin.error
    @_eraser.error
    @_extra_life.error
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
    await client.add_cog(Items(client))