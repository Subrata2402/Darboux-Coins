import discord
from discord.ext import commands
import datetime
import platform
from discord_components import *


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
        total_commands = len(self.client.commands)
        
        embed = discord.Embed(
            description = "```\n" \
                f"● Bot Latency        ::  {round(self.client.latency * 1000)}ms\n" \
                f"● Coding Language    ::  Python[{pythonVersion}]\n" \
                f"● Library Version    ::  {dpyVersion}\n" \
                f"● Bot Version        ::  1.6\n" \
                f"● Total Guilds       ::  {serverCount}\n" \
                f"● Total Users        ::  {memberCount}\n" \
                f"● Total Commands     ::  {total_commands}\n" \
                f"● Bot Developer      ::  Subrata#4099\n" \
                f"                         (660337342032248832)\n```",
            color=discord.Colour.random())
        
        # embed.add_field(name="Programing Language", value=f"[Python (Version - {pythonVersion})](https://python.org)")
        # embed.add_field(name="Discord.py Version", value=f"[{dpyVersion}](https://discord.py/version)")
        # embed.add_field(name="Total Connected Guilds", value=f"[{serverCount}](https://discord.server/count)")
        # embed.add_field(name="Total Connected Members", value=f"[{memberCount}](https://discord.member/count)")
        # embed.add_field(name="Total Connected Channels", value=f"[{channelCount}](https://discord.channel/count)")
        # embed.add_field(name="Bot Developer", value="[Schrodinger#8447](https://discord.id/702414646702768152)")
        
        embed.set_footer(text=f"Created At | {date}")
        # embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_author(name=f"{self.client.user.name}#{self.client.user.discriminator} | Bot Info !", icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        emoji = self.client.get_emoji(957904862631297085)
        embed=discord.Embed(description=f"**Click the below interaction button to invite me in your server.**", color=discord.Colour.random())
        #embed.set_thumbnail(url=self.client.user.avatar_url)
        components = [Button(style = ButtonStyle.URL, emoji = emoji, url = f"https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=523376&scope=bot", label = "Click Here to Invite")]
        await ctx.send(embed = embed, components = components)

    @commands.command(aliases=["join"])
    async def support(self, ctx):
        emoji = self.client.get_emoji(957904862631297085)
        embed=discord.Embed(description="**Click the below interaction button to join our official server for any support.**", color=discord.Colour.random())
        #embed.set_thumbnail(url=self.client.user.avatar_url)
        components = [Button(style = ButtonStyle.URL, emoji = emoji, url = "https://discord.gg/TAcEnfS8Rs", label = "Click Here to Join")]
        await ctx.send(embed = embed, components = components)
    
    @commands.command()
    @commands.is_owner()
    async def reply(self, ctx, user: discord.User=None, *, args=None):
        if not user and not args:
            return await ctx.channel.send("You didn't provide a user's id and/or a message.")
        try:
            # target = await self.client.fetch_user(user_id)
            # embed=discord.Embed(title="__Reply from Bot Owner :__", description=args, color=discord.Colour.random())
            await user.send(args)
            embed=discord.Embed(description=f"DM successfully sent to {user.name}")
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
