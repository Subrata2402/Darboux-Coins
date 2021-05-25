import discord
from discord.ext import commands
from discord.ext.commands import bot
import asyncio
import datetime
import os


class Welcome(commands.Cog):

    def __init__(self, client):
        self.bot = client


    @commands.Cog.listener()
    async def on_member_join(self, member):
        link = "www.google.com"
        date = member.created_at.__format__('%B %d, %Y %H:%M GMT')
        channel = self.bot.get_channel(831058732757942272)
        if member.guild.id == 831051146880614431:
            role = discord.utils.get(member.guild.roles, name="Darboux || Members")
            await member.add_roles(role)
            role = discord.utils.get(member.guild.roles, name="Darboux || Security")
            await member.add_roles(role)
            embed=discord.Embed(title=f"Welcome to {member.guild.name}", description=f"Hey {member.mention}, Have a great time in {member.guild.name}. Go to <#831056646176112691> and start making HQ Coins and many more for free. So stay here and enjoy!", color=discord.Colour.random())
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text=self.bot.user, icon_url=self.bot.user.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            await member.send(embed=embed)
            embed=discord.Embed(description=f"**Hello {member.mention}, Welcome to this server. Now our server has total {member.guild.member_count} members.\nHere you can make unlimited coins for HQ Trivia. Come <#831056646176112691> and type `+help` for all Commands information.**", color=discord.Colour.random())
            embed.set_author(name=member.guild.name, icon_url=member.guild.icon_url)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f"User ID: {member.id} | {date}", icon_url=member.avatar_url)
            await channel.send(embed=embed)
        else:
            embed=discord.Embed(title=f"**Welcome to {member.guild.name}**", description=f"**Hey {member.mention}, Have a great time in {member.guild.name}. Make unlimited <:extra_coins:844448578881847326> Coins for HQ Trivia Game. Get started with `-help` for more details!\n\nJoin our support server for any help use `-support` or [Click Here](https://discord.gg/TAcEnfS8Rs)**", color=discord.Colour.random())
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text=self.bot.user, icon_url=self.bot.user.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            await member.send(embed=embed)
        

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(845138450361221140)
        if member.guild.id == 831051146880614431:
            return await channel.send(f"**{member.name}#{member.discriminator}** just left the server **{member.guild.name}**")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.bot.get_channel(831058653603168286)
        embed = discord.Embed(title="**Guild Joined Information !**", color=discord.Colour.random())
        embed.add_field(name="Server Name :", value=guild.name)
        embed.add_field(name="Server Owner :", value=guild.owner)
        embed.add_field(name="Server Members :", value=guild.member_count)
        embed.set_footer(text=f"ID: {guild.id} | {guild.created_at.__format__('%B %d, %Y %H:%M GMT')}")
        embed.set_thumbnail(url=guild.icon_url)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.bot.get_channel(831058691939237938)
        embed = discord.Embed(title="**Guild Removed Information !**", color=discord.Colour.random())
        embed.add_field(name="Server Name :", value=guild.name)
        embed.add_field(name="Server Owner :", value=guild.owner)
        embed.add_field(name="Server Members :", value=guild.member_count)
        embed.set_footer(text=f"ID: {guild.id} | {guild.created_at.__format__('%B %d, %Y %H:%M GMT')}")
        embed.set_thumbnail(url=guild.icon_url)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = self.bot.get_channel(835130854740459561)
        if message.author != self.bot.user:
            embed=discord.Embed(title=f"Channel Name: `{message.channel}`\nDescription :", description=message.content, color=discord.Colour.random())
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.set_author(name=message.author, icon_url=message.author.avatar_url)
            embed.set_footer(text=f"Name: {message.author} | ID: {message.author.id}", icon_url=message.author.avatar_url)
            return await channel.send(embed=embed)
            

def setup(client):
    client.add_cog(Welcome(client))
