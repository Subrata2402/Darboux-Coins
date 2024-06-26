import discord
from discord.ext import commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from database import db

class FacebookLogin(commands.Cog, HQApi):

    def __init__(self, client):
        super().__init__()
        self.client = client

    @commands.command(aliases=["flink"])
    async def fblink(self, ctx):
        if ctx.guild: await ctx.send(f"{ctx.author.mention}, **Check your DM!**")
        embed=discord.Embed(title="**HQ Facebook Login**", description=f"**[Click Here](https://m.facebook.com/v9.0/dialog/oauth?auth_type=rerequest&cbt=1613638985174&client_id=1309867799121574&default_audience=friends&display=touch&e2e=%7B%22init%22%3A1596063.1199975831%7D&fbapp_pres=1&ies=0&nonce=EC40E5E9-148C-4D27-955B-54A3B8635F47&redirect_uri=fb1309867799121574%3A%2F%2Fauthorize%2F&response_type=id_token%2Ctoken_or_nonce%2Csigned_request%2Cgraph_domain&return_scopes=true&scope=email%2Copenid&sdk=ios&sdk_version=9.0.0&state=%7B%22challenge%22%3A%22weDSTppN3JYneIZMp63Vd71MOZ0%253D%22%2C%220_auth_logger_id%22%3A%22361441EC-F569-418B-9E84-E0703A60B519%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D) and hold to copy the link.\n\nUse `{ctx.prefix}fbmethod` to get all process of Facebook Login.**", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.author.send(embed=embed)


    @commands.command(aliases=["fblogin", "facebook", "hqflogin", "hqfblogin"])
    async def fbverify(self, ctx, token=None):
        if ctx.guild: return await ctx.send(f"{ctx.author.mention}, **You can use this command only in DM!**")
        channel = self.client.get_channel(841489971109560321)
        user_id = ctx.author.id
        if token is None:
            embed=discord.Embed(title="**HQ Facebook Login**", description=f"**[Click Here](https://m.facebook.com/v9.0/dialog/oauth?auth_type=rerequest&cbt=1613638985174&client_id=1309867799121574&default_audience=friends&display=touch&e2e=%7B%22init%22%3A1596063.1199975831%7D&fbapp_pres=1&ies=0&nonce=EC40E5E9-148C-4D27-955B-54A3B8635F47&redirect_uri=fb1309867799121574%3A%2F%2Fauthorize%2F&response_type=id_token%2Ctoken_or_nonce%2Csigned_request%2Cgraph_domain&return_scopes=true&scope=email%2Copenid&sdk=ios&sdk_version=9.0.0&state=%7B%22challenge%22%3A%22weDSTppN3JYneIZMp63Vd71MOZ0%253D%22%2C%220_auth_logger_id%22%3A%22361441EC-F569-418B-9E84-E0703A60B519%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D) and hold to copy the link.\n\nUse `{ctx.prefix}fbmethod` to get all process of Facebook Login.**", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.author.send(embed=embed)
        try:
            data = await self.facebook_login(token)
            id = data["userId"]
            username = data["username"]
            login_token = data["loginToken"]
            access_token = data["accessToken"]
        except Exception as error:
            embed=discord.Embed(title="⚠️ Api Response Error", description="This is not a valid token or token is expired. Try again with a valid token or which is not expire!", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        check_if_exist = db.profile_base.find_one({"user_id": id})
        if check_if_exist:
            embed=discord.Embed(title="⚠️ Already Exists", description="This account already exists in bot database. You can't add it again.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        user_info_dict = {
                    'id': user_id,
                    'user_id': id,
                    'access_token': access_token,
                    'login_token': login_token,
                    'username': username.lower(),
                    'auto_play': False
                }
        db.profile_base.insert_one(user_info_dict)
        embed=discord.Embed(title="Account Added ✅", description=f"Successfully add an account with name `{username}`", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)
        await channel.send(f"{ctx.author} add a account via Facebook.")

def setup(client):
    client.add_cog(FacebookLogin(client))