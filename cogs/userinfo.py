import discord, aniso8601
from discord.ext import commands
from HQApi import HQApi

class UserStats(commands.Cog(description="User Stats")):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(aliases=["user", "hqstats", "hqstat"], description="Show user stats")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def hquser(self, ctx: commands.Context, username: str = None):
        """Get any user's stats."""
        if username is None:
            return await ctx.send("Please provide username.")
        login_token = "KwmTCpQzIqiLLlxDsK7cf8mIvETtYdyofrBr4R7x6py1aH57pokb6XHdEXRcSeGk"
        try:
            api = HQApi((await api.get_tokens(login_token))["accessToken"])
            data = await api.search(username)
            id = data["data"][0]["userId"]
            data = await api.get_user(id)
            username = data["username"]
            id = data["userId"]
            avatar_url = data["avatarUrl"]
            create_at = data["created"]
            tm = aniso8601.parse_datetime(create_at).timestamp()
            total = data["leaderboard"]["total"]
            unclaimed = data["leaderboard"]["unclaimed"]
            winCount = data["winCount"]
            gamesPlayed = data["gamesPlayed"]
            highScore = data["highScore"]
            refferal = data["referralUrl"]
            embed=discord.Embed(title=f"**HQ User Stats**", color=discord.Colour.random())
            embed.add_field(name="Username", value=username)
            embed.add_field(name="User ID", value=id)
            embed.add_field(name="Created On", value=f"<t:{int(tm)}>")
            embed.add_field(name="Total Winnings", value=f"{total} (Unclaimed : {unclaimed})")
            embed.add_field(name="High Score", value=highScore)
            embed.add_field(name="Games Won", value=f"{winCount}/{gamesPlayed}")
            embed.add_field(name="Refferal Url", value=f"[Click Here]({refferal})")
            embed.set_thumbnail(url=avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)
        except:
            embed=discord.Embed(title="❎ Not Found", description=f"Couldn't find any HQ account account with name `{username}`.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)

def setup(client: commands.Bot):
    client.add_cog(UserStats(client))
