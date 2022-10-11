import discord, aniso8601
from discord.ext import commands
from HQApi import HQApi


class Show(commands.Cog(description="Show next HQ Trivia"), HQApi):

    def __init__(self, client: commands.Bot):
        super().__init__()
        self.client = client

    @commands.command(aliases=["nexthq","hqnext"], description="Show next HQ Trivia")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def nextshow(self, ctx: commands.Context):
        """Get HQ next show details."""
        response_data = await self.get_show()
        tim = (response_data["nextShowTime"])
        tm = aniso8601.parse_datetime(tim).timestamp()
        time = f"<t:{int(tm)}>"
        prize = (response_data["nextShowPrize"])
        for data in response_data["upcoming"]:
            type = data["nextShowLabel"]["title"]
        embed=discord.Embed(title="**__HQ Next Show Details !__**", description=f"**• Show Name : {type}\n• Show Time : {time}\n• Prize Money : {prize}**", color=discord.Colour.random())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/799237115962851348/816261537101905951/1200px-HQ_logo.svg.png")
        await ctx.send(embed=embed)

def setup(client: commands.Bot):
    client.add_cog(Show(client))
