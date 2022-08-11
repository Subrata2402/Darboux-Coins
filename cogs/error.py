import math
import os
import sys
import traceback
import discord
from discord.ext import commands

class Errors(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command(self, ctx):
        guild = self.client.get_guild(831051146880614431)
        if guild not in ctx.author.mutual_guilds:
            embed = discord.Embed(title = "Not Found", color = discord.Colour.random(),
                description = "You need to join our official discord server to use the bot. [Click Here](https://discord.gg/TAcEnfS8Rs) to join the server.")
            embed.set_thumbnail(url = self.client.user.avatar_url)
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            # return await ctx.send(embed = embed)
        channel = self.client.get_channel(958059478538936400)
        embed = discord.Embed(description = f"Command : `{ctx.command.name}`\nGuild : `{ctx.guild.name if ctx.guild else None}`\nChannel : `{ctx.channel.name if ctx.guild else ctx.channel}`\nCommand Failed : `{ctx.command_failed}`\nMessage :\n```\n{ctx.message.content}\n```",
                color = discord.Color.random(),
                timestamp = ctx.author.created_at)
        embed.set_footer(text = f"ID : {ctx.author.id} | Created at")
        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        if ctx.guild: embed.set_thumbnail(url = ctx.guild.icon_url)
        await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Error cog loaded successfully")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, "on_error"):
            return

        # get the original exception
        error = getattr(error, "original", error)

        if isinstance(error, commands.CommandOnCooldown):
            seconds = float("{:.2f}".format(error.retry_after))
            wait_time = f"**{'0' if seconds < 10 else ''}{seconds}** second{'s' if seconds != 1 else ''}"
            description = ctx.author.mention + ", This command is on cooldown, please retry after " + wait_time + "."
            return await ctx.send(description)
            
        if isinstance(error, commands.MaxConcurrencyReached):
            embed=discord.Embed(description=f"⚠️ You've already started a game, finish it first and then start another.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
            
        if isinstance(error, commands.TooManyArguments):
            embed = discord.Embed(
                description=f"⚠️ | You given one or more extra arguments which are not required!"
            )
            return await ctx.send(embed=embed)


        if isinstance(error, commands.NotOwner):
            embed = discord.Embed()
            embed.description = f"⚠️ | This command only for bot developers. You can't use it."
            return # await ctx.send(embed=embed)


        if isinstance(error, discord.errors.Forbidden):
            try:
                embed = discord.Embed(
                    title=f"⚠️ | Forbidden Error",
                    description=f"Error - 404 | Missing Permission(s)",
                    color=discord.Colour.random(),
                )
                await ctx.send(embed=embed)
            except discord.Forbidden:
                try:
                    embed = discord.Embed(description = f"Hey it looks like I can't send messages in {ctx.channel.mention} channel.")
                    await ctx.author.send(content = ctx.author.mention, embed = embed)
                except:
                    pass
            return

        if isinstance(error, commands.UserInputError):
            return await ctx.send(ctx.author.mention + " You provided an invalid argument. Please check the command usage and try again.")

        if isinstance(error, commands.CommandNotFound):
            return
        embed=discord.Embed(title="⚠️ Api Response Error", description=f"Something went wrong, please try again after some time.", color=discord.Colour.random())
        #embed.set_thumbnail(url=self.client.user.avatar_url)
        #embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)
        channel = await self.client.fetch_channel(958059379041640448)
        embed=discord.Embed(title=f"⚠️ | Found an error", description=f"Ignoring exception in command : `{ctx.command}`", color=discord.Colour.random())
        embed.add_field(name = "Error Detected :", value=f"```\n{error}\n```")
        embed.add_field(name = "Cog Name :", value = ctx.command.cog_name)
        try:
            await channel.send(embed=embed)
        except:
            pass
        print(f"Ignoring exception in command {ctx.command}: Cog Name : {ctx.command.cog_name}", file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
            )


def setup(client):
    client.add_cog(Errors(client))
