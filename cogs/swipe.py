import discord, asyncio
from discord.ext import commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from database import db

class Swipe(commands.Cog(description="Swipe commands")):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name="swipe", description="Swipe your account.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def swipe(self, ctx: commands.Context, username: str=None):
        """Swipe and earn extra life."""
        if username is None:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}swipe [username]` to swipe your account and earn an Extra Life.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        try:
            await ctx.message.delete()
        except:
            pass
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
        # response = await api.config()
        # enabled = response["easterEggs"]["makeItRain"]["enabled"]
        # if enabled:
        #     interval = response["easterEggs"]["makeItRain"]["interval"]
        #     hours, remainder = divmod(interval, 3600)
        #     minutes, seconds = divmod(remainder, 60)
        #     days, hours = divmod(hours, 24)
        #     if days + hours + minutes == 0:
        #         wait_time = f"**{'0' if seconds < 10 else ''}{seconds}** second{'s' if seconds != 1 else ''}"
        #     elif days + hours == 0:
        #         wait_time = f"**{'0' if minutes < 10 else ''}{minutes}** minute{'s' if minutes != 1 else ''} **{'0' if seconds < 10 else ''}{seconds}** second{'s' if seconds != 1 else ''}"
        #     elif days == 0:
        #         wait_time = f"**{'0' if hours < 10 else ''}{hours}** hour{'s' if hours != 1 else ''} **{'0' if minutes < 10 else ''}{minutes}** minute{'s' if minutes != 1 else ''} and **{'0' if seconds < 10 else ''}{seconds}** second{'s' if seconds != 1 else ''}"
        #     else:
        #         wait_time = f"**{'0' if days < 10 else ''}{days}** day{'s' if days != 1 else ''} **{'0' if hours < 10 else ''}{hours}** hour{'s' if hours != 1 else ''} **{'0' if minutes < 10 else ''}{minutes}** minute{'s' if minutes != 1 else ''} and **{'0' if seconds < 10 else ''}{seconds}** second{'s' if seconds != 1 else ''}"
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
            await x.edit(embed=embed)


def setup(client: commands.Bot):
    client.add_cog(Swipe(client))
