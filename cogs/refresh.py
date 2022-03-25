import discord
from discord.ext import commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from database import db

class Refresh(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Refresh"])
    async def refresh(self, ctx, username=None):
        """Refresh an account.."""
        if username is None:
            embed=discord.Embed(title="⚠️ Invalid Argument", description=f"You didn't put username after `{ctx.prefix}refresh`. Please use correct : `{ctx.prefix}refresh [username]`", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        check_if_exist = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()})
        if not check_if_exist:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await x.edit(embed=embed)
        embed=discord.Embed(title="Refreshing...", color=discord.Colour.random())
        x = await ctx.send(embed=embed)
        try:
            api = HQApi()
            token = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()}).get("login_token")
            data = await api.get_tokens(token)
            name = data["username"]
            access_token = data["accessToken"]
            update = ({'access_token': access_token, 'username': name.lower()})
            db.profile_base.update_one({'username': username}, {'$set': update})
            embed=discord.Embed(title="Successfully refreshed your account ✅", color=discord.Colour.random())
            await x.edit(embed=embed)
        except Exception as e:
            embed=discord.Embed(title="Refreshing Failed!", color=discord.Colour.random())
            await x.edit(embed=embed)


def setup(client):
    client.add_cog(Refresh(client))
