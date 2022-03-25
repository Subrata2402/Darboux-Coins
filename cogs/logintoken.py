import discord
from discord.ext import commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from database import db

class LoginToken(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def getlt(self, ctx, username:str):
        """Get login token."""
        api = HQApi(db.profile_base.find_one({"username": username.lower()}).get("access_token"))
        data = await api.get_login_token()
        lt = data["loginToken"]
        await ctx.send(f"```\n{lt}\n```")


def setup(client):
    client.add_cog(LoginToken(client))
