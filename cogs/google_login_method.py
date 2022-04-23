import discord, datetime
from discord.ext import commands
from config.button import peginator_button

class GoogleLoginMethod(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def gmethod(self, ctx):
        if ctx.guild:
            return await ctx.send(f"{ctx.author.mention}, **You can use this command only in DM!**")

        first_page_buttons = await peginator_button(self.client, disabled_1 = True, disabled_2 = True)
        last_page_buttons = await peginator_button(self.client, disabled_3 = True, disabled_4 = True)
        middle_page_buttons = await peginator_button(self.client)
        

        embed1=discord.Embed(title="**__HQ Google Login Method__**", description=f"**Hey {ctx.author.mention}, Thanks for using {self.client.user.mention} Bot. Follow these steps to link your HQ Trivia account with bot by Google Account.\n\nUse below emojis to change the page and get the process of Google Login Method.**", color=discord.Colour.random())
        embed1.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        embed1.set_thumbnail(url=self.client.user.avatar_url)
        embed1.timestamp = datetime.datetime.utcnow()

        embed2=discord.Embed(title="**__Step - 1__**", description=f"**Use `{ctx.prefix}google` in DM to initiate login with Google Account. You will be sent a login link by the bot. Click this link to login with Google Account.**", color=discord.Colour.random())
        embed2.set_image(url="https://media.discordapp.net/attachments/827262575439380542/967343072323182642/IMG_20220423_140503.jpg")
        embed2.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        embed2.timestamp = datetime.datetime.utcnow()

        embed3=discord.Embed(title="**__Step -2__**", description=f'**After Click the link you will get an page which will say "Choose an account to continue to [HQ Trivia](https://hqtrivia.com)". Choose an google account which you want to login with HQ Trivia.**', color=discord.Colour.random())
        embed3.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        embed3.timestamp = datetime.datetime.utcnow()
        embed3.set_image(url="https://media.discordapp.net/attachments/838633900950552606/956008699820908574/unknown.jpeg")
        
        embed4=discord.Embed(title="**__Step - 3__**", description=f'**After choose an account you will get an error page like the below image. Click and hold your finger on the "localhost:8080". A link will be copied.**', color=discord.Colour.random())
        embed4.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        embed4.timestamp = datetime.datetime.utcnow()
        embed4.set_image(url="https://media.discordapp.net/attachments/838633900950552606/857251778872606720/IMG_20210623_184934.jpg")
        
        embed5=discord.Embed(title="**__Step - 4__**", description=f'**Then use `{ctx.prefix}google <copied link>` and successfully add your HQ Trivia account in bot database. Use `{ctx.prefix}accounts` to check your all save accounts.**', color=discord.Colour.random())
        embed5.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        embed5.timestamp = datetime.datetime.utcnow()
        embed5.set_image(url="https://media.discordapp.net/attachments/827262575439380542/967343072063127574/IMG_20220423_140538.jpg")
        
        

        pages = [embed1, embed2, embed3, embed4, embed5]

        message = await ctx.send(embed = embed1, components = first_page_buttons)

        def check(interaction):
            return interaction.author == ctx.author and interaction.message == message
        i = 0
        while True:
            try:
                interaction = await self.client.wait_for("button_click", timeout = 45.0, check = check)
            except:
                buttons = await peginator_button(client = self.client, disabled_1 = True, disabled_2 = True, disabled_3 = True, disabled_4 = True)
                return await message.edit(components = buttons)
            if interaction.custom_id == "button1":
                i = 0
            elif interaction.custom_id == "button2":
                if i > 0:
                    i -= 1
            elif interaction.custom_id == "button3":
                if i < 4:
                    i += 1
            elif interaction.custom_id == "button4":
                i = 4
                
            if i == 0:
                await interaction.respond(type = 7, embed = pages[i], components = first_page_buttons)
            elif i == 4:
                await interaction.respond(type = 7, embed = pages[i], components = last_page_buttons)
            else:
                await interaction.respond(type = 7, embed = pages[i], components = middle_page_buttons)


def setup(client):
    client.add_cog(GoogleLoginMethod(client))
