import discord, multiprocessing
from discord.ext import commands
import asyncio, threading
import time, datetime
import sys, traceback, os
from discord_components import *
from Trivia.swagbucks import client_one, client_two

class DarbouxCoins(commands.Cog):
    
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

bot_prefix = "-", "+", "."
intents = discord.Intents.all()
ids = [790190926630486016, 660337342032248832]
client = commands.Bot(command_prefix = bot_prefix, intents=intents, strip_after_prefix=True, owner_ids = ids, case_insensitive = True)
client.remove_command('help')
DiscordComponents(client)
client.add_cog(DarbouxCoins(client))

@client.event
async def on_message(message):
    cmd = client.get_command(message.content[1:].strip().lower().partition(' ')[0])
    if cmd:
        guild = self.client.get_guild(831051146880614431)
        if guild not in message.author.mutual_guilds:
            embed = discord.Embed(title = "❎ Not Found", color = discord.Colour.random(),
                description = "You need to join our official discord server to use the bot. [Click Here](https://discord.gg/TAcEnfS8Rs) to join the server.")
            embed.set_thumbnail(url = client.user.avatar_url)
            embed.set_footer(text = message.author, icon_url = message.author.avatar_url)
            return await ctx.send(embed = embed)
    if message.channel.id == 831051147472666636: return
    if message.author.id == 433615162394804224 and message.channel.id == 844547681838039041:
        for embed in message.embeds:
            to_dict = embed.to_dict()
            embed.description = to_dict["description"] + f"\n**Source :** [Click Here]({to_dict['url']})"
            embed.color = discord.Colour.random()
            embed.set_footer(text = "HQ Tweets", icon_url = "https://media.discordapp.net/attachments/827262575439380542/976439492644843610/625974899051069460.png")
            embed.set_thumbnail(url = "")
            embed.set_author(icon_url = to_dict["thumbnail"]["url"], name = to_dict["author"]["name"])
            embed.timestamp = datetime.datetime.utcnow()
            await client.get_channel(976420002020343838).send(embed = embed, content = "<@&1005187248284778567>")
    if message.content.startswith(client.user.mention):
        await message.channel.send(f"Hey {message.author.mention}, My prefix is `-` For more information use `-help`")
    await client.process_commands(message)

extensions = [
        "login", "show", "hqname", "welcome", "swipe", "google_login_method",
        "logintoken", "token", "payout", "dcplay", "balance", "self_roles",
        "editname", "userinfo", "details", "help", "general",
        "rwin", "refresh", "friend", "sdcplay", "items", "error",
        "fblogin", "glogin", "profile", "fb_login_method", "autoplay"
    ]

if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension("cogs." + extension)
        except Exception as e:
            print(f"Error loading {extension}", file=sys.stderr)
            traceback.print_exc()

client.run(os.getenv("darboux_token"))
# darboux_thread = multiprocessing.Process(target = client.run, args = (os.getenv("darboux_token"), ))
# client_one_thread = multiprocessing.Process(target = client_one().run, args = (os.getenv("bot_token_1"), ))
# client_two_thread = multiprocessing.Process(target = client_two().run, args = (os.getenv("bot_token_2"), ))

# darboux_thread.start()
# client_one_thread.start()
# client_two_thread.start()

# darboux_thread.join()
# client_one_thread.join()
# client_two_thread.join()
