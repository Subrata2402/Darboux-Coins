import discord
from discord.ext import commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from database import db

class Token(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def getact(self, ctx, username:str):
        """Get random access token."""
        token = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()}).get("login_token")
        api = HQApi()
        data = await api.get_tokens(token)
        access_token = data["accessToken"]
        await ctx.send(f"```\n{access_token}\n```")

    
    @commands.command(pass_context=True, aliases=['addt'])
    async def addtoken(self, ctx, token=None):
        """Add token in bot database."""
        if token is None:
            embed=discord.Embed(title="⚠️ Invalid Argument", description=f"You didn't put token after `{ctx.prefix}addtoken`. Please use correct : `{ctx.prefix}addtoken [token]`", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        if ctx.guild: return await ctx.send(f"{ctx.author.mention}, **You can add token with bot only in DM's.**")
        try:
            api = HQApi(token)
            data = await api.get_users_me()
            username = data["username"]
            id = data["userId"]
            user_id = ctx.author.id
            data = await api.get_login_token()
            login_token = data["loginToken"]
            access_token = token
        except ApiResponseError:
            embed=discord.Embed(title="⚠️ Api Response Error", description="This is not a valid token or token is expired. Try again with a valid token or which is not expire!", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        check_if_exist = db.profile_base.find_one({"id": user_id, "user_id": id})
        if check_if_exist == None:
            user_info_dict = {
                        'id': user_id,
                        'user_id': id,
                        'access_token': access_token,
                        'login_token': login_token,
                        'username': username.lower(),
                        'auto_play': False
                    }
            db.profile_base.insert_one(user_info_dict)
            embed=discord.Embed(title="Account Added ✅", description=f"Successfully add an account with name `{username}` in bot database.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)
            channel = self.client.get_channel(841489971109560321)
            await channel.send(f"{ctx.author} add a account via access token.")
        else:
            embed=discord.Embed(title="⚠️ Already Exists", description=f"This account already exists in bot database with name `{username}`. You can't add it again.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    async def token(self, ctx, username=None):
        """Get save access token."""
        if username is None:
            embed=discord.Embed(title="⚠️ Invalid Argument", description=f"You didn't put username after `{ctx.prefix}token`. Please use correct : `{ctx.prefix}token [username]`", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        return await ctx.send("This command is temporary disabled!")
        check_if_exist = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()})
        if check_if_exist:
            spec_user_token = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()}).get("access_token")
            #embed=discord.Embed(title=f"{username} | Access Token", description=f"`{spec_user_token}`", color=discord.Colour.random())
            #embed.set_thumbnail(url=self.client.user.avatar_url)
            #embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.author.send(f"**{username} | Access Token**\n```\n{spec_user_token}\n```")
            if ctx.guild: await ctx.send(f"{ctx.author.mention}, Check your DM!")
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Token(client))
