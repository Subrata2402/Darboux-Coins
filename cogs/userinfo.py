import discord, aniso8601
from discord.ext import commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from database import db

class UserStats(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["user", "hqstats", "hqstat"])
    async def hquser(self, ctx, name:str):
        """Get any user's stats."""
        login_token = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()}).get("login_token")
        api = HQApi()
        data = await api.get_tokens(login_token)
        access_token = data["accessToken"]
        try:
            api = HQApi(access_token)
            data = await api.search(name)
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
            embed=discord.Embed(title="❎ Not Found", description=f"Couldn't find any HQ account account with name `{name}`.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(UserStats(client))
