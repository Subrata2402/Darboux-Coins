import discord, aniso8601
from discord.ext import commands
from HQApi import HQApi


class Show(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["nexthq","hqnext"])
    async def nextshow(self, ctx):
        """Get HQ next show details."""
        api = HQApi()
        response_data = await api.get_show()
        tim = (response_data["nextShowTime"])
        tm = aniso8601.parse_datetime(tim).timestamp()
        time = f"<t:{int(tm)}>"
        prize = (response_data["nextShowPrize"])
        for data in response_data["upcoming"]:
            type = data["nextShowLabel"]["title"]
        embed=discord.Embed(title="**__HQ Next Show Details !__**", description=f"**• Show Name : {type}\n• Show Time : {time}\n• Prize Money : {prize}**", color=discord.Colour.random())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/799237115962851348/816261537101905951/1200px-HQ_logo.svg.png")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Show(client))
