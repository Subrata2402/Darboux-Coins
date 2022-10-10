import discord
import asyncio
import bot_config
from discord.ext import commands
import sys
import traceback
discord.utils.setup_logging()


initial_extensions = [
        "cogs.general",
        "cogs.glogin",
        "cogs.fblogin",
        "cogs.details",
        "cogs.editname",
        "cogs.autoplay",
        "cogs.balance",
        "cogs.items",
        "cogs.payout",
        "cogs.token",
        "cogs.swipe",
        "cogs.show",
        "cogs.userinfo",
    ]

class DarbouxCoins(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix = bot_config.BOT_PREFIX,
            intents = discord.Intents(guilds = True, members = True, messages = True),#, message_content = True),
            case_insensitive = True,
            strip_after_prefix = True,
        )
        
    async def on_ready(self):
        print("Bot is ready!")
        channel = self.get_channel(bot_config.UPDATE_CHANNEL_ID)
        embed = discord.Embed(
            title="Bot Updated ✅", description="Bot successfully updated. No issues found!", color=discord.Colour.random())
        embed.set_thumbnail(url=self.user.avatar.url)
        embed.set_footer(text=self.user,
                         icon_url=self.user.avatar.url)
        await channel.send(embed=embed)
        await self.change_presence(status=discord.Status.offline, activity=discord.Game(name="For play offair trivia -dcplay <username>"))
        # await self.change_presence(status=discord.Status.dnd, activity=discord.Game(name="For play offair trivia -dcplay <username>", type=2))
        # await asyncio.sleep(5)
        # await self.change_presence(status=discord.Status.idle, activity=discord.Game(name="For Help ➜ -help", type=2))
        # await asyncio.sleep(5)
        # await self.change_presence(status=discord.Status.dnd, activity=discord.Game(name="For add account with Google -google <response_link>", type=2))
        # await asyncio.sleep(5)
        # await self.client.change_presence(status=discord.Status.idle, activity=discord.Game(name="For add account with Facebook -facebook <token>", type=2))
        # await asyncio.sleep(5)

    async def setup_hook(self) -> None:
        print(f"{self.user} has connected to Discord!")
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
                # initial_extensions.remove(extension)
            except Exception as error:
                print(f"Error loading {extension}", file=sys.stderr)
                traceback.print_exc()
        # if not initial_extensions:
        #     print("Extensions loaded successful!")
        # else:
        #     print("Failed to load some extensions : {}".format(initial_extensions))
        await self.tree.sync() # guild = discord.Object(id = bot_config.GUILD_ID))
        print("Commands synced successful!")
        
    async def start_client(self):
        await self.start(bot_config.BOT_TOKEN)


asyncio.run(DarbouxCoins().start_client())
            

#     @commands.command(
#         name="say",
#         description="Send message by bot.",
#         aliases=["tell", "echo"],
#         usage="[message]",
#         brief="Hello, what's up!"
#     )
#     @commands.is_owner()
#     async def say(self, ctx, *, message):
#         await ctx.message.delete()
#         await ctx.send(message)

#     @commands.command(
#         name="sayembed",
#         description="Send message with embed.",
#         aliases=[],
#         usage="",
#         brief=""
#     )
#     @commands.is_owner()
#     async def sayem(self, ctx, *, message):
#         """Send Message With Embed."""
#         await ctx.message.delete()
#         embed = discord.Embed(description=message,
#                               color=discord.Colour.random())
#         await ctx.send(embed=embed)

# bot_prefix = "-", "+", "."
# intents = discord.Intents.all()
# ids = [790190926630486016, 660337342032248832]
# client = commands.Bot(command_prefix=bot_prefix, intents=intents,
#                       strip_after_prefix=True, owner_ids=ids, case_insensitive=True)
# client.remove_command('help')
# client.add_cog(DarbouxCoins(client))


# @client.event
# async def on_message(message):
#     cmd = client.get_command(
#         message.content[1:].strip().lower().partition(' ')[0])
#     if cmd:
#         guild = client.get_guild(831051146880614431)
#         if not message.author.bot and guild not in message.author.mutual_guilds:
#             embed = discord.Embed(title="❎ Not Found", color=discord.Colour.random(),
#                                   description="You need to join our official discord server to use the bot. [Click Here](https://discord.gg/TAcEnfS8Rs) to join the server.")
#             embed.set_thumbnail(url=client.user.avatar_url)
#             embed.set_footer(text=message.author,
#                              icon_url=message.author.avatar_url)
#             return await message.channel.send(embed=embed)
#     if message.channel.id == 831051147472666636:
#         return
#     if message.author.id == 433615162394804224 and message.channel.id == 844547681838039041:
#         for embed in message.embeds:
#             to_dict = embed.to_dict()
#             embed.description = to_dict["description"] + \
#                 f"\n**Source :** [Click Here]({to_dict['url']})"
#             embed.color = discord.Colour.random()
#             embed.set_footer(
#                 text="HQ Tweets", icon_url="https://media.discordapp.net/attachments/827262575439380542/976439492644843610/625974899051069460.png")
#             embed.set_thumbnail(url="")
#             embed.set_author(
#                 icon_url=to_dict["thumbnail"]["url"], name=to_dict["author"]["name"])
#             embed.timestamp = datetime.datetime.utcnow()
#             await client.get_channel(976420002020343838).send(embed=embed, content="<@&1005187248284778567>")
#     if message.content.startswith(client.user.mention):
#         await message.channel.send(f"Hey {message.author.mention}, My prefix is `-` For more information use `-help`")
#     await client.process_commands(message)

# extensions = [
#     "login", "show", "hqname", "welcome", "swipe", "google_login_method",
#     "logintoken", "token", "payout", "dcplay", "balance", "self_roles",
#     "editname", "userinfo", "details", "help", "general", "test",
#     "rwin", "refresh", "friend", "sdcplay", "items", "error",
#     "fblogin", "glogin", "profile", "fb_login_method", "autoplay"
# ]

# if __name__ == "__main__":
#     for extension in extensions:
#         try:
#             client.load_extension("cogs." + extension)
#         except Exception as e:
#             print(f"Error loading {extension}", file=sys.stderr)
#             traceback.print_exc()

# # client.load_extension("Trivia.swagbucks")
# client.run('ODM4NjMxODUyNjAzNDc0MDAx.G-9Duv._dakrmlLG0XjcuFlVItFC53scMApXZugMhUpdQ')
