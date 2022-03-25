import discord
from discord.ext import commands
import datetime
import platform


class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='stats', description='Sends some bot stats', aliases=['botstat','botstats','botinfo'])
    async def stats(self, ctx):
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.client.guilds)
        memberCount = len(set(self.client.get_all_members()))
        channelCount = len(set(self.client.get_all_channels()))
        date = self.client.user.created_at.__format__("%b %d, %Y %I:%M %p")
        s = 0
        for x in self.client.commands:
            s = s + 1
        
        embed = discord.Embed(description=f"● **Bot Latency :** {round(self.client.latency * 1000)}ms\n● **Coding Language :** Python[{pythonVersion}]\n● **Discord.py Version :** {dpyVersion}\n● **Bot Version :** 1.5\n● **Total Guilds :** {serverCount}\n● **Total Users :** {memberCount}\n● **Total Commands :** {s}\n● **Developer :** Subrata#3250", color=discord.Colour.random())
        """embed.add_field(name="Programing Language", value=f"[Python (Version - {pythonVersion})](https://python.org)")
        embed.add_field(name="Discord.py Version", value=f"[{dpyVersion}](https://discord.py/version)")
        embed.add_field(name="Total Connected Guilds", value=f"[{serverCount}](https://discord.server/count)")
        embed.add_field(name="Total Connected Members", value=f"[{memberCount}](https://discord.member/count)")
        embed.add_field(name="Total Connected Channels", value=f"[{channelCount}](https://discord.channel/count)")
        embed.add_field(name="Bot Developer", value="[Schrodinger#8447](https://discord.id/702414646702768152)")"""
        embed.set_footer(text=f"Created At | {date}")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_author(name=f"{self.client.user.name}#{self.client.user.discriminator} | Bot Info !", icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        embed=discord.Embed(title="**Invite Me to Your Server !**", description="**Invite Link : [Click Here](https://discord.com/api/oauth2/authorize?client_id=838631852603474001&permissions=523376&scope=bot)**", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["join"])
    async def support(self, ctx):
        embed=discord.Embed(title="**Join Our Official Server !**", description="**Join Link : [Click Here](https://discord.gg/TAcEnfS8Rs)**", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.is_owner()
    async def reply(self, ctx, user_id=None, *, args=None):
        if user_id != None and args != None:
            return await ctx.channel.send("You didn't provide a user's id and/or a message.")
        try:
            target = await self.client.fetch_user(user_id)
            #embed=discord.Embed(title="__Reply from Bot Owner :__", description=args, color=discord.Colour.random())
            await target.send(args)
            embed=discord.Embed(description=f"DM successfully sent to {target.name}")
            await ctx.channel.send(embed=embed)
        except:
            await ctx.channel.send("Couldn't dm the given user.")
       
    @commands.command()
    async def report(self, ctx, *, msg=None):
        if msg is None:
            return await ctx.send("Please specify a message to send.")
        member = await self.client.fetch_channel(844801172518731796)
        embed=discord.Embed(title="__Report :__", description=msg, color=discord.Colour.random())
        embed.set_footer(text=f"User ID: {ctx.author.id}")
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.timestamp = (datetime.datetime.utcnow())
        await member.send(embed=embed)
        embed2=discord.Embed(description=f"Report successfully sent ✅\nReport: {msg}")
        await ctx.send(embed=embed2)

    @commands.command()
    async def suggest(self, ctx, *, message=None):
        if message is None:
            return await ctx.send("Please specify a message to send.")
        member = await self.client.fetch_channel(844801103132098580)
        embed=discord.Embed(title="__Suggestion :__", description=message, color=discord.Colour.random())
        embed.set_footer(text=f"User ID: {ctx.author.id}")
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.timestamp = (datetime.datetime.utcnow())
        msg = await member.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        embed2=discord.Embed(description=f"Suggestion successfully sent ✅\nSuggestion: {message}")
        await ctx.send(embed=embed2)
            
    @commands.command()
    async def feedback(self, ctx, *, message=None):
        if message is None:
            return await ctx.send("Please specify a message to send.")
        member = await self.client.fetch_channel(844803633967005737)
        embed=discord.Embed(title="__Feedback :__", description=message, color=discord.Colour.random())
        embed.set_footer(text=f"User ID: {ctx.author.id}")
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.timestamp = (datetime.datetime.utcnow())
        await member.send(embed=embed)
            
        embed2=discord.Embed(description=f"Feedback successfully sent. Thanks for your feedback.")
        await ctx.send(embed=embed2)


def setup(client):
    client.add_cog(Help(client))
