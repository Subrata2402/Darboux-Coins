import sys
import traceback
import discord
import bot_config
from discord.ext import commands
from discord import app_commands
from HQApi import HQApi
from database import db

class FacebookLogin(commands.Cog, HQApi):

    def __init__(self, client):
        super().__init__()
        self.client = client

    # @app_commands.command(name="fblogin", description="Login to HQ Trivia using Facebook.")
    # async def _fblink(self, interaction: discord.Interaction):
    #     """Login to HQ Trivia using Facebook."""
    #     facebook_login_link = "https://m.facebook.com/v9.0/dialog/oauth?auth_type=rerequest&cbt=1613638985174&client_id=1309867799121574&default_audience=friends&display=touch&e2e=%7B%22init%22%3A1596063.1199975831%7D&fbapp_pres=1&ies=0&nonce=EC40E5E9-148C-4D27-955B-54A3B8635F47&redirect_uri=fb1309867799121574%3A%2F%2Fauthorize%2F&response_type=id_token%2Ctoken_or_nonce%2Csigned_request%2Cgraph_domain&return_scopes=true&scope=email%2Copenid&sdk=ios&sdk_version=9.0.0&state=%7B%22challenge%22%3A%22weDSTppN3JYneIZMp63Vd71MOZ0%253D%22%2C%220_auth_logger_id%22%3A%22361441EC-F569-418B-9E84-E0703A60B519%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D"
    #     description = f"**[Click Here]({facebook_login_link})** and hold for 2 seconds to copy the link.\n\n"
    #     embed = discord.Embed(title="Facebook Login", description=description, color=discord.Colour.random())
        # if ctx.guild: await ctx.send(f"{ctx.author.mention}, **Check your DM!**")
        # ) and hold to copy the link.\n\nUse `{ctx.prefix}fbmethod` to get all process of Facebook Login.**", color=discord.Colour.random())
        # embed.set_thumbnail(url=self.client.user.avatar_url)
        # embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        # await ctx.author.send(embed=embed)


    @app_commands.command(name="hqfblogin", description="Login to HQ Trivia using Facebook.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(token="The token you got from Facebook Login.")
    async def _hq_facebook_login(self, interaction: discord.Interaction, token: str=None):
        """Login to HQ Trivia using Facebook."""
        if interaction.guild:
            return await interaction.response.send_message(bot_config.dm_message(interaction))
        if not token:
            facebook_login_link = "https://m.facebook.com/v9.0/dialog/oauth?auth_type=rerequest&cbt=1613638985174&client_id=1309867799121574&default_audience=friends&display=touch&e2e=%7B%22init%22%3A1596063.1199975831%7D&fbapp_pres=1&ies=0&nonce=EC40E5E9-148C-4D27-955B-54A3B8635F47&redirect_uri=fb1309867799121574%3A%2F%2Fauthorize%2F&response_type=id_token%2Ctoken_or_nonce%2Csigned_request%2Cgraph_domain&return_scopes=true&scope=email%2Copenid&sdk=ios&sdk_version=9.0.0&state=%7B%22challenge%22%3A%22weDSTppN3JYneIZMp63Vd71MOZ0%253D%22%2C%220_auth_logger_id%22%3A%22361441EC-F569-418B-9E84-E0703A60B519%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D"
            description = f"**[Click Here]({facebook_login_link})** and hold for 2 seconds to copy the link.\n\n" \
                          f"If you don't know how to login, please visit this channel: <#843359251963052033>"
            embed = discord.Embed(title="Facebook Login", description=description, color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar.url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar.url)
            return await interaction.response.send_message(embed=embed)
        await interaction.response.send_message("This command is under development.")

        # if ctx.guild: return await ctx.send(f"{ctx.author.mention}, **You can use this command only in DM!**")
        # channel = self.client.get_channel(841489971109560321)
        # user_id = ctx.author.id
        # if token is None:
        #     embed=discord.Embed(title="**HQ Facebook Login**", description=f"**[Click Here](https://m.facebook.com/v9.0/dialog/oauth?auth_type=rerequest&cbt=1613638985174&client_id=1309867799121574&default_audience=friends&display=touch&e2e=%7B%22init%22%3A1596063.1199975831%7D&fbapp_pres=1&ies=0&nonce=EC40E5E9-148C-4D27-955B-54A3B8635F47&redirect_uri=fb1309867799121574%3A%2F%2Fauthorize%2F&response_type=id_token%2Ctoken_or_nonce%2Csigned_request%2Cgraph_domain&return_scopes=true&scope=email%2Copenid&sdk=ios&sdk_version=9.0.0&state=%7B%22challenge%22%3A%22weDSTppN3JYneIZMp63Vd71MOZ0%253D%22%2C%220_auth_logger_id%22%3A%22361441EC-F569-418B-9E84-E0703A60B519%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D) and hold to copy the link.\n\nUse `{ctx.prefix}fbmethod` to get all process of Facebook Login.**", color=discord.Colour.random())
        #     embed.set_thumbnail(url=self.client.user.avatar_url)
        #     embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        #     return await ctx.author.send(embed=embed)
        # try:
        #     data = await self.facebook_login(token)
        #     id = data["userId"]
        #     username = data["username"]
        #     login_token = data["loginToken"]
        #     access_token = data["accessToken"]
        # except Exception as error:
        #     embed=discord.Embed(title="⚠️ Api Response Error", description="This is not a valid token or token is expired. Try again with a valid token or which is not expire!", color=discord.Colour.random())
        #     embed.set_thumbnail(url=self.client.user.avatar_url)
        #     embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        #     return await ctx.send(embed=embed)
        # check_if_exist = db.profile_base.find_one({"user_id": id})
        # if check_if_exist:
        #     embed=discord.Embed(title="⚠️ Already Exists", description="This account already exists in bot database. You can't add it again.", color=discord.Colour.random())
        #     embed.set_thumbnail(url=self.client.user.avatar_url)
        #     embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        #     return await ctx.send(embed=embed)
        # user_info_dict = {
        #             'id': user_id,
        #             'user_id': id,
        #             'access_token': access_token,
        #             'login_token': login_token,
        #             'username': username.lower(),
        #             'auto_play': False
        #         }
        # db.profile_base.insert_one(user_info_dict)
        # embed=discord.Embed(title="Account Added ✅", description=f"Successfully add an account with name `{username}`", color=discord.Colour.random())
        # embed.set_thumbnail(url=self.client.user.avatar_url)
        # embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        # await ctx.send(embed=embed)
        # await channel.send(f"{ctx.author} add a account via Facebook.")

    @_hq_facebook_login.error
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
    await client.add_cog(FacebookLogin(client))