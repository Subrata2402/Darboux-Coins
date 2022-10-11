import discord
from discord.ext import commands
from discord import app_commands
import bot_config

class ButtonClass(discord.ui.Button):

    def __init__(self, emojis: list[discord.PartialEmoji], disabled: bool):
        self.emojis = emojis
        super().__init__(timeout=None)

    @discord.ui.button(self.emojis[0], style=discord.ButtonStyle.blue, custom_id="button_1")


class HelpCommands(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client


    @app_commands.command(name="help", description="Get a list of all commands.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def _help(self, interaction: discord.Interaction):
        """Get a list of all commands."""
        await interaction.response.defer()
        embed1 = discord.Embed(color=discord.Colour.random())
        embed1.add_field(name=f"/add +[country code][number]", value="> To save your HQ Trivia account in bot.", inline = False)
        embed1.add_field(name=f"/addtoken [bearer token]", value="> Add your HQ Trivia account in bot with bearer token.", inline = False)
        embed1.add_field(name=f"/facebook (fbtoken)", value="> Add your HQ Trivia account in bot with Facebook access token.", inline = False)
        embed1.add_field(name=f"/google (response url)", value="> Add your HQ Trivia account in bot with Google response url.", inline = False)
        embed1.add_field(name=f"/dcplay [username]", value="> Play HQ Trivia Daily Challenge and wins 48/48 to get you 400 {bot_config.emoji.extra_coins} Coins.", inline = False)
        embed1.add_field(name=f"/sdcplay [username]", value="> Play HQ Trivia Daily Challenge in Slowmode and wins 48/48 to get you 400 {bot_config.emoji.extra_coins} Coins.", inline = False)
        embed1.add_field(name=f"/autoplay [username] [enable/disable]", value="> Toggle on/off for auto playing Daily Challenge for coins (Max. 1500 Coins).", inline = False)
        embed1.set_thumbnail(url=self.client.user.avatar.url)
        embed1.set_author(name="| Darboux Coins Help Menu !", icon_url=self.client.user.avatar.url)
        embed1.set_footer(text=f"embed : 01/05 | Total Commands : 07", icon_url=interaction.user.avatar.url)

        embed2 = discord.Embed(color=discord.Colour.random())
        embed2.add_field(name=f"/accounts", value="> To check, how many accounts you have added in the bot.", inline = False)
        embed2.add_field(name=f"/token [username]", value="> Get bearer token of your HQ account.", inline = False)
        embed2.add_field(name=f"/details [username]", value="> Get details of your HQ Trivia account.", inline = False)
        embed2.add_field(name=f"/hquser [username]", value="> Get any HQ user's info.", inline = False)
        embed2.add_field(name=f"/remove [username]", value="> Remove your HQ Trivia account from the bot database.", inline = False)
        embed2.add_field(name=f"/removeall", value="> Remove all saved accounts from bot database.", inline = False)
        embed2.add_field(name=f"/refresh [username]", value="> Refresh your HQ account if token is expired.", inline = False)
        embed2.add_field(name=f"/profile", value="> Shows you a list of accounts that are logged into the bot.", inline = False)
        embed2.set_thumbnail(url=self.client.user.avatar.url)
        embed2.set_author(name="| Darboux Coins Help Menu !", icon_url=self.client.user.avatar.url)
        embed2.set_footer(text=f"embed : 02/05 | Total Commands : 08", icon_url=interaction.user.avatar.url)

        embed3 = discord.Embed(color=discord.Colour.random())
        embed3.add_field(name=f"/life [username] [amount: 1/3/5]", value=f"> Purchase Extra {bot_config.emoji.extra_life} Life using {bot_config.emoji.extra_coins} Coins.", inline = False)
        embed3.add_field(name=f"/eraser [username] [amount: 1/3/5]", value=f"> Purchase Extra {bot_config.emoji.erasers} Eraser using {bot_config.emoji.extra_coins} Coins.", inline = False)
        embed3.add_field(name=f"/superspin [username] [amount: 1/3/5]", value=f"> Purchase Extra {bot_config.emoji.super_spin} Super-spin using {bot_config.emoji.extra_coins} Coins.", inline = False)
        embed3.add_field(name=f"/swipe [username]", value=f"> Swiped your HQ account to earn an Extra {bot_config.emoji.extra_life} Life.", inline = False)
        embed3.add_field(name=f"/cashout [username] [email_id]", value="> 💸 Cashout your winnings in your paypal account.", inline = False)
        embed3.add_field(name=f"/payout [username]", value="> Get last 10 💸 cashout details of your HQ account.", inline = False)
        embed3.add_field(name=f"/balance", value="> Get total 💰 balance & 💸 cashout details of all accounts.", inline = False)
        embed3.add_field(name=f"/recentwins [username]", value="> Get last 30 winnings of your HQ account.", inline = False)
        embed3.set_thumbnail(url=self.client.user.avatar.url)
        embed3.set_author(name="| Darboux Coins Help Menu !", icon_url=self.client.user.avatar.url)
        embed3.set_footer(text=f"embed : 03/05 | Total Commands : 08", icon_url=interaction.user.avatar.url)

        embed4 = discord.Embed(color=discord.Colour.random())
        embed4.add_field(name=f"/addfriend [username] [friend's username]", value="> Send friend request.", inline = False)
        embed4.add_field(name=f"/editname [username] [new_name]", value="> Edit your HQ account username.", inline = False)
        embed4.add_field(name=f"/friends [username]", value="> Get your HQ friends list.", inline = False)
        embed4.add_field(name=f"/acceptfriend [username] [friend's username]", value="> Accept friend request.", inline = False)
        embed4.add_field(name=f"/removefriend [username] [friend's username]", value="> Remove a friend from your friends list.", inline = False)
        embed4.add_field(name=f"/friendstatus [username] [friend's username]", value="> Check your friend's status.", inline = False)
        embed4.add_field(name=f"/hqname", value="> Get random US Name for HQ.", inline = False)
        embed4.add_field(name=f"/nextshow", value="> Get HQ Next Show details.", inline = False)
        embed4.set_thumbnail(url=self.client.user.avatar.url)
        embed4.set_author(name="| Darboux Coins Help Menu !", icon_url=self.client.user.avatar.url)
        embed4.set_footer(text=f"embed : 04/05 | Total Commands : 08", icon_url=interaction.user.avatar.url)

        embed5 = discord.Embed(color=discord.Colour.random())
        embed5.add_field(name=f"/report [message]", value="> Report your issues.", inline = False)
        embed5.add_field(name=f"/suggest [message]", value="> Suggest your suggestion.", inline = False)
        embed5.add_field(name=f"/feedback [message]", value="> Give your feedback.", inline = False)
        embed5.add_field(name=f"/botinfo", value="> Get the information about bot.", inline = False)
        embed5.add_field(name=f"/donate", value="> Donate some money.", inline = False)
        embed5.add_field(name=f"/invite", value="> Invite bot in your server.", inline = False)
        embed5.add_field(name=f"/join", value="> Join our official bot server.", inline = False)
        embed5.set_thumbnail(url=self.client.user.avatar.url)
        embed5.set_author(name="| Darboux Coins Help Menu !", icon_url=self.client.user.avatar.url)
        embed5.set_footer(text=f"embed : 05/05 | Total Commands : 07", icon_url=interaction.user.avatar.url)

        embeds = [embed1, embed2, embed3, embed4, embed5]

#         message = await ctx.send(embed = embed1, components = first_embed_buttons)

#         def check(interaction):
#             return interaction.author == interaction.user and interaction.message == message
#         i = 0
#         while True:
#             try:
#                 interaction = await self.client.wait_for("button_click", timeout = 45.0, check = check)
#             except:
#                 buttons = await peginator_button(client = self.client, disabled_1 = True, disabled_2 = True, disabled_3 = True, disabled_4 = True)
#                 return await message.edit(components = buttons)
#             if interaction.custom_id == "button1":
#                 i = 0
#             elif interaction.custom_id == "button2":
#                 if i > 0:
#                     i -= 1
#             elif interaction.custom_id == "button3":
#                 if i < 4:
#                     i += 1
#             elif interaction.custom_id == "button4":
#                 i = 4
                
#             if i == 0:
#                 await interaction.respond(type = 7, embed = embeds[i], components = first_embed_buttons)
#             elif i == 4:
#                 await interaction.respond(type = 7, embed = embeds[i], components = last_embed_buttons)
#             else:
#                 await interaction.respond(type = 7, embed = embeds[i], components = middle_embed_buttons)


# def setup(client):
#     client.add_cog(Help(client))
