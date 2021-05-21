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
        role = discord.utils.get(member.guild.roles, name="Darboux || Members")
        await member.add_roles(role)
        role = discord.utils.get(member.guild.roles, name="Darboux || Security")
        await member.add_roles(role)
        embed=discord.Embed(description=f"**Hello {member.mention}, Welcome to this server. Now our server has total {member.guild.member_count} members.\nHere you can make unlimited coins for HQ Trivia. Come <#831056646176112691> and type `+help` for all Commands information.**", color=0x00FFFF)
        #embed.add_field(name="**__Description :__**", value=f"**Thanks `{member.name}` for join this server, have a nice day! Invite your friends and support this server.**")
        embed.set_author(name=member.guild.name, icon_url=member.guild.icon_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"User ID: {member.id} | {date}", icon_url=member.avatar_url)
        #embed.set_image(url=f"https://api.xzusfin.repl.co/card?avatar={member.avatar_url}&middle=Welcome&name={member.name}&bottom=Now+Our+Server+has+{member.guild.member_count}+members&background=https://cdn.discordapp.com/attachments/817427539135168562/817678318132264990/2c33e4c7167d0086420abfe69eb4a42b.jpg")
        await channel.send(embed=embed)
        #await channel.send(f"https://api.xzusfin.repl.co/card?avatar={member.avatar_url}&middle=Welcome&name={member.name}&bottom=Now+Our+Server+has+{member.guild.member_count}+members&background=https://cdn.discordapp.com/attachments/817427539135168562/817678318132264990/2c33e4c7167d0086420abfe69eb4a42b.jpg")
        #await channel.send(f"**{member.name}#{member.discriminator}** just joined **{member.guild.name}**")
        #await member.send(f"Hey {member.mention}, Welcome to **{member.guild.name}**! Thanks for Joining 👍👍\nType `+help` to get started.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(831058602198171658)
        await channel.send(f"**{member.name}#{member.discriminator}** just left the server **{member.guild.name}**")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.bot.get_channel(831058653603168286)
        embed = discord.Embed(title="**Guild Joined Information !**", color=0x00FFFF)
        embed.add_field(name="Server Name :", value=guild.name)
        embed.add_field(name="Server Owner :", value=guild.owner)
        embed.add_field(name="Server Members :", value=guild.member_count)
        embed.set_footer(text=f"ID: {guild.id} | {guild.created_at.__format__('%B %d, %Y %H:%M GMT')}")
        embed.set_thumbnail(url=guild.icon_url)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.bot.get_channel(831058691939237938)
        embed = discord.Embed(title="**Guild Removed Information !**", color=0x00FFFF)
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
            embed=discord.Embed(title=f"Channel Name: `{message.channel}`\nDescription :", description=message.content, color=0x000000)
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.set_author(name=message.author, icon_url=message.author.avatar_url)
            embed.set_footer(text=f"Name: {message.author} | ID: {message.author.id}", icon_url=message.author.avatar_url)
            return await channel.send(embed=embed)
            

def setup(client):
    client.add_cog(Welcome(client))
