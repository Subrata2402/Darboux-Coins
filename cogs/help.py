import discord
from discord.ext import commands
from config.button import peginator_button

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def help(self, ctx):
        first_page_buttons = await peginator_button(self.client, disabled_1 = True, disabled_2 = True)
        last_page_buttons = await peginator_button(self.client, disabled_3 = True, disabled_4 = True)
        middle_page_buttons = await peginator_button(self.client)
        
        page1 = discord.Embed(color=discord.Colour.random())
        page1.add_field(name=f"{ctx.prefix}add +(country code)(number)", value="> To save your HQ Trivia account in bot.")
        page1.add_field(name=f"{ctx.prefix}addtoken (bearer token)", value="> Add your HQ Trivia account in bot with bearer token.")
        #page1.add_field(name=f"{ctx.prefix}fblink", value="> Get HQ Facebook Login Link.")
        page1.add_field(name=f"{ctx.prefix}facebook (fbtoken)", value="> Add your HQ Trivia account in bot with Facebook access token.")
        #page1.add_field(name=f"{ctx.prefix}glink", value="> Get HQ Google Login Link.")
        page1.add_field(name=f"{ctx.prefix}google (response url)", value="> Add your HQ Trivia account in bot with Google response url.")
        page1.add_field(name=f"{ctx.prefix}dcplay (username)", value="> Play HQ Trivia Daily Challenge and wins 48/48 to get you 400 <:extra_coins:844448578881847326> Coins.")
        page1.add_field(name=f"{ctx.prefix}sdcplay (username)", value="> Play HQ Trivia Daily Challenge in Slowmode and wins 48/48 to get you 400 <:extra_coins:844448578881847326> Coins.")
        page1.set_thumbnail(url=self.client.user.avatar_url)
        page1.set_author(name="| Darboux Coins Help Menu !", icon_url=self.client.user.avatar_url)
        page1.set_footer(text=f"Page : 01/05 | Total Commands : 06", icon_url=ctx.author.avatar_url)

        page2 = discord.Embed(color=discord.Colour.random())
        page2.add_field(name=f"{ctx.prefix}accounts", value="> To check, how many accounts you have added in the bot.")
        page2.add_field(name=f"{ctx.prefix}token (username)", value="> Get bearer token of your HQ account.")
        page2.add_field(name=f"{ctx.prefix}details (username)", value="> Get details of your HQ Trivia account.")
        page2.add_field(name=f"{ctx.prefix}hquser (username)", value="> Get any HQ user's info.")
        page2.add_field(name=f"{ctx.prefix}remove (username)", value="> Remove your HQ Trivia account from the bot database.")
        page2.add_field(name=f"{ctx.prefix}removeall", value="> Remove all saved accounts from bot database.")
        page2.add_field(name=f"{ctx.prefix}refresh (username)", value="> Refresh your HQ account if token is expired.")
        page2.add_field(name=f"{ctx.prefix}profile", value="> Shows you a list of accounts that are logged into the bot.")
        page2.set_thumbnail(url=self.client.user.avatar_url)
        page2.set_author(name="| Darboux Coins Help Menu !", icon_url=self.client.user.avatar_url)
        page2.set_footer(text=f"Page : 02/05 | Total Commands : 08", icon_url=ctx.author.avatar_url)

        page3 = discord.Embed(color=discord.Colour.random())
        page3.add_field(name=f"{ctx.prefix}life (username) [amount]", value="> Purchase Extra <:extra_life:844448511264948225> Life using <:extra_coins:844448578881847326> Coins.")
        page3.add_field(name=f"{ctx.prefix}eraser (username) [amount]", value="> Purchase Extra <:eraser:844448550498205736> Eraser using <:extra_coins:844448578881847326> Coins.")
        page3.add_field(name=f"{ctx.prefix}superspin (username) [amount]", value="> Purchase Extra <:super_spin:844448472908300299> Super-spin using <:extra_coins:844448578881847326> Coins.")
        page3.add_field(name=f"{ctx.prefix}swipe (username)", value="> Swiped your HQ account to earn an Extra <:extra_life:844448511264948225> Life.")
        page3.add_field(name=f"{ctx.prefix}cashout (email_id) (username)", value="> 💸 Cashout your winnings in your paypal account.")
        page3.add_field(name=f"{ctx.prefix}payout (username)", value="> Get last 10 💸 cashout details of your HQ account.")
        page3.add_field(name=f"{ctx.prefix}balance", value="> Get total 💰 balance & 💸 cashout details of all accounts.")
        page3.add_field(name=f"{ctx.prefix}recentwins (username)", value="> Get last 30 winnings of your HQ account.")
        page3.set_thumbnail(url=self.client.user.avatar_url)
        page3.set_author(name="| Darboux Coins Help Menu !", icon_url=self.client.user.avatar_url)
        page3.set_footer(text=f"Page : 03/05 | Total Commands : 08", icon_url=ctx.author.avatar_url)

        page4 = discord.Embed(color=discord.Colour.random())
        page4.add_field(name=f"{ctx.prefix}addfriend (username) (friend's username)", value="> Send friend request.")
        page4.add_field(name=f"{ctx.prefix}editname (username) (new_name)", value="> Edit your HQ account username.")
        page4.add_field(name=f"{ctx.prefix}friends (username)", value="> Get your HQ friends list.")
        page4.add_field(name=f"{ctx.prefix}acceptfriend (username) (friend's username)", value="> Accept friend request.")
        page4.add_field(name=f"{ctx.prefix}removefriend (username) (friend's username)", value="> Remove a friend from your friends list.")
        page4.add_field(name=f"{ctx.prefix}friendstatus (username) (friend's username)", value="> Check your friend's status.")
        page4.add_field(name=f"{ctx.prefix}hqname", value="> Get random US Name for HQ.")
        page4.add_field(name=f"{ctx.prefix}nextshow", value="> Get HQ Next Show details.")
        page4.set_thumbnail(url=self.client.user.avatar_url)
        page4.set_author(name="| Darboux Coins Help Menu !", icon_url=self.client.user.avatar_url)
        page4.set_footer(text=f"Page : 04/05 | Total Commands : 08", icon_url=ctx.author.avatar_url)

        page5 = discord.Embed(color=discord.Colour.random())
        page5.add_field(name=f"{ctx.prefix}report (message)", value="> Report your issues.")
        page5.add_field(name=f"{ctx.prefix}suggest (message)", value="> Suggest your suggestion.")
        page5.add_field(name=f"{ctx.prefix}feedback (message)", value="> Give your feedback.")
        page5.add_field(name=f"{ctx.prefix}botinfo", value="> Get the information about bot.")
        page5.add_field(name=f"{ctx.prefix}invite", value="> Invite bot in your server.")
        page5.add_field(name=f"{ctx.prefix}join", value="> Join our official bot server.")
        page5.set_thumbnail(url=self.client.user.avatar_url)
        page5.set_author(name="| Darboux Coins Help Menu !", icon_url=self.client.user.avatar_url)
        page5.set_footer(text=f"Page : 05/05 | Total Commands : 06", icon_url=ctx.author.avatar_url)

        pages = [page1, page2, page3, page4, page5]

        message = await ctx.send(embed = page1, components = first_page_buttons)

        def check(interaction):
            return interaction.author == ctx.author and interaction.message == message
        i = 0
        while True:
            try:
                interaction = await self.client.wait_for("button_click", timeout = 45.0, check = check)
            except:
                buttons = await peginator_button(client = self.client, disabled_1 = True, disabled_2 = True, disabled_3 = True, disabled_4 = True)
                return await message.edit(components = buttons)
            if interaction.custom_id == "button_4":
                i = 0
            elif interaction.custom_id == "button_3":
                if i > 0:
                    i -= 1
            elif interaction.custom_id == "button_2":
                if i < 4:
                    i += 1
            else:
                i = 4
                
            if i == 0:
                await interaction.respond(type = 7, embed = pages[i], components = first_page_buttons)
            elif i == 4:
                await interaction.respond(type = 7, embed = pages[i], components = last_page_buttons)
            else:
                await interaction.respond(type = 7, embed = pages[i], components = middle_page_buttons)

def setup(client):
    client.add_cog(Help(client))
