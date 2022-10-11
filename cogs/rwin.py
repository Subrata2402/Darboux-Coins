import discord, aniso8601
from discord.ext import commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from database import db

class RecentWins(commands.Cog(description="Recent Wins")):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name="recentwins", description="Get your recent wins", aliases=["rwins"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def recentwins(self, ctx: commands.Context, username: str = None):
        """Get recent winnings."""
        if not username: return await ctx.send(f"{ctx.author.mention}, you didn't enter any username.")
        try:
            await ctx.message.delete()
        except:
            pass
        check_if_exist = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()})
        if check_if_exist:
            try:
                api = HQApi(db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()}).get("access_token"))
                data = await api.get_users_me()
            except ApiResponseError:
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            username = data["username"]
            data = await api.get_payouts_me()
            description_info=f""
            for index, rwin in enumerate(data["recentWins"]):
                if index+1 > 30:
                    break
                prize = rwin["prize"]
                windate = rwin["winDate"]
                tm = aniso8601.parse_datetime(windate).timestamp()
                x_time = f"<t:{int(tm)}>"
                description_info += f"**{index+1}. {x_time} : {prize}**\n"
            embed=discord.Embed(title=f"**__{username}'s Winnings Info !__**", description=description_info, color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.author.send(embed=embed)
            if ctx.guild: await ctx.send(f"{ctx.author.mention}, **Check your DM!**")
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)


def setup(client: commands.Bot):
    client.add_cog(RecentWins(client))
