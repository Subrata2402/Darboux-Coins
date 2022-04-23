import discord, datetime
from discord.ext import commands
import DiscordUtils

class GoogleLoginMethod(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def gmethod(self, ctx):
        if ctx.guild:
            return await ctx.send(f"{ctx.author.mention}, **You can use this command only in DM!**")

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
        
        

        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx)
        paginator.add_reaction('⏮', "first")
        paginator.add_reaction('◀', "back")
        #paginator.add_reaction('<:emoji_60:855472859034943488>', "lock")
        paginator.add_reaction('▶', "next")
        paginator.add_reaction('⏭', "last")
        embeds = [embed1, embed2, embed3, embed4, embed5]
        await paginator.run(embeds)

def setup(client):
    client.add_cog(GoogleLoginMethod(client))
