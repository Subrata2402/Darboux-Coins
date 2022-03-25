import discord, requests, json
from discord.ext import commands


class HQName(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hqname(self, ctx):
        """Get HQ Random US Name."""
        embed=discord.Embed(title="Random US Name Generator", color=discord.Colour.random())
        embed.add_field(name="Name:", value="Generating...")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=embed)
        r = requests.get("https://api.namefake.com")
        res = r.json()
        name = res["name"]
        embed=discord.Embed(title="Random US Name Generator", color=discord.Colour.random())
        embed.add_field(name="Name:", value=name)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        await msg.edit(embed=embed)

def setup(client):
    client.add_cog(HQName(client))
