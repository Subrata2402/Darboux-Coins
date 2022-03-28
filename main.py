import discord
from discord.ext import commands
import asyncio
import time
import sys, traceback
from discord_components import *

class Darboux(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('====================')
        print(self.client.user)
        channel = self.client.get_channel(835743589241454592)
        embed=discord.Embed(title="Bot Updated ✅", description="Bot successfully updated. No issues found!", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await channel.send(embed=embed)
        while True:
            #await self.client.change_presence(activity=discord.Activity(type=3,name="on "+str(len(self.client.guilds))+" servers | -invite"))
            #await asyncio.sleep(5)
            await self.client.change_presence(status=discord.Status.online, activity=discord.Game(name="with -dcplay <username>", type=2))
            await asyncio.sleep(5)
            await self.client.change_presence(status=discord.Status.online, activity=discord.Game(name="with Help ➜ -help", type=2))
            await asyncio.sleep(5)
            await self.client.change_presence(status=discord.Status.dnd, activity=discord.Game(name="with -google <response_link>", type=2))
            await asyncio.sleep(5)
            await self.client.change_presence(status=discord.Status.idle, activity=discord.Game(name="with -facebook <token>", type=2))
            await asyncio.sleep(5)

    @commands.command(
        name = "say",
        description = "Send message by bot.",
        aliases = ["tell", "echo"],
        usage = "[message]",
        brief = "Hello, what's up!"
        )
    @commands.is_owner()
    async def say(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)
        
    @commands.command(
        name = "sayembed",
        description = "Send message with embed.",
        aliases = [],
        usage = "",
        brief = ""
        )
    @commands.is_owner()
    async def sayem(self, ctx, *, message):
        """Send Message With Embed."""
        await ctx.message.delete()
        embed=discord.Embed(description=message, color=discord.Colour.random())
        await ctx.send(embed=embed)
    
    @commands.command(
        name = "ping",
        description = "Get bot latency.",
        aliases = ["pong"],
        usage = "",
        brief = ""
        )
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        message = await ctx.send("**__Pong!__**")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"**__Pong!__** :ping_pong:  **{int(ping)}ms**")

bot_prefix = "-", "+"
intents = discord.Intents.all()
ids = [790190926630486016, 660337342032248832]
client = commands.Bot(command_prefix = bot_prefix, intents=intents, strip_after_prefix=True, owner_ids = ids, case_insensitive = True)
client.remove_command('help')
DiscordComponents(client)
client.add_cog(Darboux(client))

@client.event
async def on_message(message):
   if message.content.startswith(client.user.mention):
       await message.channel.send(f"Hey {message.author.mention}, My prefix is `-` For more information use `-help`")
   await client.process_commands(message)

extensions = [
        "cogs.login", "cogs.show", "cogs.hqname", "cogs.welcome", "cogs.swipe", "cogs.google_login_method",
        "cogs.logintoken", "cogs.token", "cogs.payout", "cogs.dcplay", "cogs.balance",
        "cogs.editname", "cogs.userinfo", "cogs.details", "cogs.help", "cogs.general",
        "cogs.rwin", "cogs.refresh", "cogs.friend", "cogs.sdcplay", "cogs.items", "cogs.error",
        "cogs.fblogin", "cogs.glogin", "cogs.profile", "cogs.fb_login_method", "cogs.autoplay"
    ]

if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            print(f"Error loading {extension}", file=sys.stderr)
            traceback.print_exc()

token = "ODI1OTU1OTEzMDcyNTA4OTY5.YGFdYw.qGXROAOU_QQUh0UN3WwDZGsPBGE"
client.run(token)
