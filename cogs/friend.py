import discord
from discord.ext import commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from database import db

class Friends(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def friends(self, ctx, username=None):
        """Get friend lists."""
        if username is None:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}friends [username]` to check your all friends list.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        check_id = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()})
        if not check_id:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        if ctx.guild:
            await ctx.send(f"{ctx.author.mention}, **Check your DM!**")
        try:
            api = HQApi(db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()}).get("access_token"))
            data = await api.get_users_me()
        except ApiResponseError:
            embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.author.send(embed=embed)
        username = data["username"]
        response = await api.friend_list()
        embed1=discord.Embed(title=f"**__{username}'s Friends List !__**", color=discord.Colour.random())
        embed2=discord.Embed(color=discord.Colour.random())
        embed3=discord.Embed(color=discord.Colour.random())
        embed=discord.Embed(title=f"Loading {username}'s friends list...", color=discord.Colour.random())
        x = await ctx.author.send(embed=embed)
        for index, data in enumerate(response["data"]):
            name = data["username"]
            total = data["leaderboard"]["total"]
            highScore = data["highScore"]
            gamesPlayed = data["gamesPlayed"]
            winCount = data["winCount"]
            name = f"{index+1}. {name}"
            value = f"> Total Winnings : {total}\n> High Score : {highScore}\n> Games Won : {winCount}/{gamesPlayed}"
            if s < 21:
                embed1.add_field(name=name, value=value)
            elif s < 41:
                embed2.add_field(name=name, value=value)
            else:
                embed3.add_field(name=name, value=value)
        if s == 0:
            embed=discord.Embed(title=f"**__{username}'s Friends List !__**", description=f"Couldn't find any friends in your friend list.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.author.send(embed=embed)
        if s > 0:
            embed1.set_thumbnail(url=self.client.user.avatar_url)
            embed1.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await x.edit(embed=embed1)
        if s > 20:
            embed2.set_thumbnail(url=self.client.user.avatar_url)
            embed2.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.author.send(embed=embed2)
        if s > 40:
            embed3.set_thumbnail(url=self.client.user.avatar_url)
            embed3.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.author.send(embed=embed3)

        

    @commands.command()
    async def addfriend(self, ctx, username=None, name=None):
        """Send friend request."""
        if not username or not name:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}addfriend [username] [friend's username]` to send a friend request.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        commander_id = ctx.author.id
        name_list = []
        all_data = list(token_base.find({"id": commander_id, "username": username}))
        for i in all_data:
            name_list.append(i['username'])
        if username in name_list:
            token = token_base.find_one({'username': username})['token']
            try:
                api = HQApi(token)
                data = api.search(name)
                id = data["data"][0]["userId"]
            except ApiResponseError:
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            try:
                data = api.add_friend(id)
                embed=discord.Embed(title="**Request Send Done ✅**", description=f"**Successfully sent friend request to `{name}`**", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
            except:
                embed=discord.Embed(title="**Request Send Failed ⚠️**", description=f"**Couldn't sent Friend Request to `{name}`.**", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)


    @commands.command()
    async def acceptfriend(self, ctx, username=None, name=None):
        """Accept friend request."""
        if not username or not name:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}acceptfriend [username] [friend's username]` to accept a friend request.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        commander_id = ctx.author.id
        name_list = []
        all_data = list(token_base.find({"id": commander_id, "username": username}))
        for i in all_data:
            name_list.append(i['username'])
        if username in name_list:
            token = token_base.find_one({'username': username})['token']
            try:
                api = HQApi(token)
                data = api.search(name)
                id = data["data"][0]["userId"]
            except ApiResponseError:
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            try:
                data = api.accept_friend(id)
                embed=discord.Embed(title="**Friend Request Accepted ✅**", description=f"**Successfully accept friend request `{name}`**", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
            except:
                embed=discord.Embed(title="**Failed to Request Accept ⚠️**", description=f"**Couldn't find user `{name}`.**", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)


    @commands.command()
    async def removefriend(self, ctx, username=None, name=None):
        """Remove a Friend from your friends list."""
        if not username or not name:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}removefriend [username] [friend's username]` to remove a friend from your friends list.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        commander_id = ctx.author.id
        name_list = []
        all_data = list(token_base.find({"id": commander_id, "username": username}))
        for i in all_data:
            name_list.append(i['username'])
        if username in name_list:
            token = token_base.find_one({'username': username})['token']
            try:
                api = HQApi(token)
                data = api.search(name)
                id = data["data"][0]["userId"]
            except ApiResponseError:
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            try:
                data = api.remove_friend(id)
                embed=discord.Embed(title="**Friend Removed ✅**", description=f"**Successfully friend removed `{name}`**", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
            except:
                embed=discord.Embed(title="**Failed to Remove Friend ⚠️**", description=f"**Couldn't find user `{name}`.**", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)


    @commands.command()
    async def friendstatus(self, ctx, username=None, name=None):
        """Get friends stats."""
        if not username or not name:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}friendstatus [username] [Friend's username]` to check your friend's status.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        commander_id = ctx.author.id
        name_list = []
        all_data = list(token_base.find({"id": commander_id, "username": username}))
        for i in all_data:
            name_list.append(i['username'])
        if username in name_list:
            token = token_base.find_one({'username': username})['token']
            try:
                api = HQApi(token)
                data = api.search(name)
                id = data["data"][0]["userId"]
            except ApiResponseError:
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            data = api.friend_status(id)
            stats = data['status']
            if stats == "None":
                stats = f"{name} is not your friend."
            elif stats == "FRIENDS":
                stats = f"{name} is your friend."
            elif stats == "INBOUND_REQUEST":
                stats = "Incoming friend request. You did not accept his/her friend request."
            elif stats == "OUTBOUND_REQUEST":
                stats = "Outgoing friend request. He/She did not accept your friend request."
            else:
                stats = f"{name} is not your friend."
            embed=discord.Embed(title=f"__Friend Status of {username}__", description=stats, color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Friends(client))
