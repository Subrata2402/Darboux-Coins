import sys
import traceback
import discord
from discord.ext import commands
from HQApi import HQApi
from database import db
import bot_config
from discord import app_commands


class EditUsername(commands.Cog):

    def __init__(self, client):
        self.client = client

    @app_commands.command(name="editname", description="Edit your username.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(username="Username of the account.", new_username="New username of the account.")
    async def _edit_name(self, interaction: discord.Interaction, username: str, new_username: str):
        """Edit your username."""
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
        try:
            data = await api.edit_username(new_username)
            update = {"username": new_username.lower()}
            await db.profile_base.update_one({"id": interaction.user.id, "username": username.lower()}, {"$inc": update})
            embed=discord.Embed(title="**Username Edited Done ✅**", description=f"Successfully Edited username `{username}` to `{new_username}`", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar.url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
            await interaction.followup.send(embed=embed)
        except:
            embed=discord.Embed(title="**Username Edited Failed ⚠️**", description=f"This username is not available. Please try again with another username.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar.url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
            await interaction.followup.send(embed=embed)
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `+accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar.url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
            await interaction.followup.send(embed=embed)


    @_edit_name.error
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
    await client.add_cog(EditUsername(client))