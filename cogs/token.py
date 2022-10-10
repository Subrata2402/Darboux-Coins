import sys
import traceback
import discord
from discord.ext import commands
from discord import app_commands
from HQApi import HQApi
from database import db
import bot_config

class Token(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    # @commands.command()
    # @commands.is_owner()
    # async def getact(self, ctx, username:str):
    #     """Get random access token."""
    #     token = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()}).get("login_token")
    #     api = HQApi()
    #     data = await api.get_tokens(token)
    #     access_token = data["accessToken"]
    #     await ctx.send(f"```\n{access_token}\n```")

    
    @app_commands.command(name="token", description="Add an account with access token.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(token="Access token of the account.")
    async def _add_token(self, interaction: discord.Interaction, token: str):
        """Add an account with access token."""
        await interaction.response.defer()
        if interaction.guild:
            return await interaction.followup.send(bot_config.dm_message(interaction))
        api = HQApi(token)
        data = await api.get_users_me()
        if data.get("error"):
            if data["errorCode"] == 102:
                return await interaction.followup.send("This is not a valid token or token is expired. Try again with a valid token or which is not expire!")
            else:
                return await interaction.followup.send(f"```\n{data['error']}\n```")
        username = data["username"]
        id = data["userId"]
        user_id = interaction.user.id
        data = await api.get_login_token()
        login_token = data["loginToken"]
        access_token = token
        check_if_exist = await db.profile_base.find_one({"id": user_id, "user_id": id})
        if check_if_exist:
            return await interaction.followup.send("This account is already added in your profile. You can't add same account twice.")
        user_info_dict = {
                    'id': user_id,
                    'user_id': id,
                    'access_token': access_token,
                    'login_token': login_token,
                    'username': username.lower(),
                    'auto_play': False
                }
        await db.profile_base.insert_one(user_info_dict)
        embed=discord.Embed(title="Account Added ✅", description=f"Successfully add an account with name `{username}` in bot database.", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await interaction.followup.send(embed=embed)
        channel = self.client.get_channel(bot_config.ACC_ADD_CHANNEL_ID)
        await channel.send(f"{interaction.user} add a account via access token.")


    @app_commands.command(name="get_token", description="Get your access token.") 
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(username="Username of the account.")
    async def _get_token(self, interaction: discord.Interaction, username: str):
        """Get your access token."""
        await interaction.response.defer()
        if interaction.guild:
            return await interaction.followup.send(bot_config.dm_message(interaction))
        user_id = interaction.user.id
        check_if_exist = await db.profile_base.find_one({"id": user_id, "username": username.lower()})
        if not check_if_exist:
            return await interaction.followup.send(bot_config.account_not_found_message(username))
        access_token = check_if_exist.get("access_token")
        embed=discord.Embed(title=f"{username} | Access Token", description=f"```\n{access_token}\n```", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await interaction.followup.send(embed=embed)


    @_add_token.error
    @_get_token.error
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
    await client.add_cog(Token(client))
