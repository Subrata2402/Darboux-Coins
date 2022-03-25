import discord, asyncio
from discord.ext import commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from database import db

class Swipe(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def swipe(self, ctx, username=None):
        """Swipe and earn extra life."""
        if username is None:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}swipe [username]` to swipe your account and earn an Extra Life.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        check_if_exist = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()})
        if not check_if_exist:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        try:
            api = HQApi(db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()}).get("access_token"))
            data = await api.get_users_me()
        except ApiResponseError:
            embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        embed=discord.Embed(title=f"Swiping...", color=discord.Colour.random())
        x = await ctx.send(embed=embed)
        await asyncio.sleep(2)
        try:
            r = await api.swipe()
            data = r["data"]
            embed=discord.Embed(title="Swiped Done ✅", description=f"You have successfully swiped your account and earn an Extra <:extra_life:844448511264948225> Life.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await x.edit(embed=embed)
        except:
            embed=discord.Embed(title="⚠️ Swiped Failed", description=f"You have already swiped your account in this month.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await x.edit(embed=embed)


def setup(client):
    client.add_cog(Swipe(client))
