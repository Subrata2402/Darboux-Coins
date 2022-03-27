import discord
from discord.ext import commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from database import db


class EditUsername(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def editname(self, ctx, username=None, name=None):
        """Edit username."""
        if not username or not name:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}editname [username] [new name]` to edit your HQ Trivia account username.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        try:
            await ctx.message.delete()
        except:
            pass
        check_id = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()})
        if check_id:
            try:
                api = HQApi(db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()}).get("access_token"))
                data = await api.get_users_me()
            except ApiResponseError:
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            try:
                data = await api.edit_username(name)
                update = {"username": name.lower()}
                db.profile_base.update_one({"id": ctx.author.id, "username": username.lower()}, {"$set": update})
                embed=discord.Embed(title="**Username Edited Done ✅**", description=f"Successfully Edited username `{username}` to `{name}`", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
            except:
                embed=discord.Embed(title="**Username Edited Failed ⚠️**", description=f"This username is not available. Please try again with another username.", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `+accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(EditUsername(client))
