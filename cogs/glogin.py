import discord
from discord.ext import commands
from HQApi import HQApi
import aiohttp
from database import db
from urllib.parse import unquote

class Google(commands.Cog(description="Login HQ with Google"), HQApi):

    def __init__(self, client: commands.Bot):
        super().__init__()
        self.client = client

    async def get_id_token(self, url: str) -> str:
        """Get id_token from url."""
        try:
            access_token = url.split("?code=")[1].split("&scope")[0]
        except:
            return None
        url = 'https://www.googleapis.com/oauth2/v4/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        code = unquote(access_token)
        data = {
            "audience": '137603896957-05igbd6ktod5h41kscji39jpgbsi3lk8.apps.googleusercontent.com',
            "client_id": '137603896957-80gmmo4fdcm9u5d68p6885r189lurufk.apps.googleusercontent.com',
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": "com.googleusercontent.apps.137603896957-80gmmo4fdcm9u5d68p6885r189lurufk:/oauth2callback",
            "verifier": '47328508'
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url = url, headers = headers, data = data) as response:
                if response.status != 200: return None
                response = await response.json()
                id_token = response.get("id_token")
                return id_token
        

    # @commands.command(aliases=["googlelink"])
    # async def glink(self, ctx):
    #     if ctx.guild:
    #         await ctx.send(f"{ctx.author.mention}, **Check your DM!**")
    #     with open("Video/VID-20220713-WA0000.mp4", "rb") as f:
    #         file = discord.File(f, filename = "add-account-with-google.mp4", spoiler = False)
    #         embed=discord.Embed(title="**HQ Google Login**", description=f"**[Click Here](https://accounts.google.com/o/oauth2/v2/auth?audience=668326540387-84isqp5u1s4dubes1tns5i7p2kgqefja.apps.googleusercontent.com&client_id=668326540387-isfa1c5ibd6h0mhm2h10n242q2uc131q.apps.googleusercontent.com&response_type=code&scope=email%20profile&&redirect_uri=http://localhost:8080&verifier=56778634) to login HQ Trivia with Google Account.\n\nUse `{ctx.prefix}gmethod` to get all process of Google Login.**", color=discord.Colour.random())
    #         #embed.add_field(name="Login Link", value="[Click Here](87-isfa1c5ibd6h0mhm2h10n242q2uc131q.apps.googleusercontent.com&response_type=code&scope=email%20profile&&redirect_uri=https://localhost:8000&verifier=56778634)")
    #         embed.set_thumbnail(url=self.client.user.avatar_url)
    #         embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
    #         await ctx.author.send(embed=embed, file = file)


    @commands.command(aliases=["glinkverify","googleverify","glogin","hqgverify", "google", "glink"], description="Login HQ with Google")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def gverify(self, ctx: commands.Context, url: str = None):
        """Login HQ with Google."""
        if ctx.guild:
            return await ctx.send(f"{ctx.author.mention}, **You can use this command only in DM!**")
        if url is None:
            with open("Video/VID-20220713-WA0000.mp4", "rb") as f:
                file = discord.File(f, filename = "add-account-with-google.mp4", spoiler = False)
                embed=discord.Embed(title="**HQ Google Login**",
                    description=f"**[Click Here](https://accounts.google.com/o/oauth2/v2/auth?audience=137603896957-05igbd6ktod5h41kscji39jpgbsi3lk8.apps.googleusercontent.com&response_type=code&scope=email%20profile&verifier=47328508&redirect_uri=com.googleusercontent.apps.137603896957-80gmmo4fdcm9u5d68p6885r189lurufk%3A%2Foauth2callback&client_id=137603896957-80gmmo4fdcm9u5d68p6885r189lurufk.apps.googleusercontent.com) and hold for 2 seconds to copy the link. Then see the tutorial video and follow the steps to add your HQ Trivia account in bot." \
                    f"\n\n[Click Here](https://play.google.com/store/apps/details?id=com.prodevutils.inspecto) to download [Inspecto - The Dev Browser (Beta)](https://play.google.com/store/apps/details?id=com.prodevutils.inspecto). " \
                    "\n\nIf the application doesn't work then try one with this application. [Click Here](https://play.google.com/store/apps/details?id=com.eruda) to download [Eruda - Browser Console.](https://play.google.com/store/apps/details?id=com.eruda)**",
                    color=discord.Colour.random())
                #embed.add_field(name="Login Link", value="[Click Here](https://accounts.google.com/o/oauth2/v2/auth?audience=137603896957-05igbd6ktod5h41kscji39jpgbsi3lk8.apps.googleusercontent.com&response_type=code&scope=email%20profile&verifier=47328508&redirect_uri=com.googleusercontent.apps.137603896957-80gmmo4fdcm9u5d68p6885r189lurufk%3A%2Foauth2callback&client_id=137603896957-80gmmo4fdcm9u5d68p6885r189lurufk.apps.googleusercontent.com)")
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await ctx.author.send(embed=embed)
                return await ctx.author.send(file = file)
        user_id = ctx.author.id
        channel = self.client.get_channel(841489971109560321)
        id_token = await self.get_id_token(url)
        if not id_token:
            return await ctx.send(ctx.author.mention + ", **Invalid URL provided!**")
        data = await self.google_login(id_token)
        id = data["userId"]
        username = data["username"]
        login_token = data["loginToken"]
        access_token = data["accessToken"]
        check_if_exist = db.profile_base.find_one({"id": ctx.author.id, "user_id": id})
        if check_if_exist:
            embed=discord.Embed(title="⚠️ Already Exists", description="This account already exists in bot database. You can't add it again.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        user_info_dict = {
                    'id': user_id,
                    'user_id': id,
                    'access_token': access_token,
                    'login_token': login_token,
                    'username': username.lower(),
                    'auto_play': False
                }
        db.profile_base.insert_one(user_info_dict)
        embed=discord.Embed(title="Account Added ✅", description=f"Successfully add an account with name `{username}`", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)
        await channel.send(f"{ctx.author} add a account via Google.")

def setup(client: commands.Bot):
    client.add_cog(Google(client))
