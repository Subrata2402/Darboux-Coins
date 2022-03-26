import discord, math, datetime
from discord.ext import commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from database import db
from config.button import peginator_button

class Friends(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def friends(self, ctx, username=None):
        """Get friend lists."""
        first_page_buttons = await peginator_button(self.client, disabled_1 = True, disabled_2 = True)
        last_page_buttons = await peginator_button(self.client, disabled_3 = True, disabled_4 = True)
        middle_page_buttons = await peginator_button(self.client)
        
        if username is None:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}friends [username]` to check your all friends list.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        check_id = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()})
        if not check_id:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        if ctx.guild: await ctx.send(f"{ctx.author.mention}, **Check your DM!**")
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
        embed=discord.Embed(title=f"Loading {username}'s friends list...", color=discord.Colour.random())
        message = await ctx.author.send(embed=embed)
        embed=discord.Embed(title=f"**__{username}'s Friends List !__**", color=discord.Colour.random())
        friends_data = response["data"]
        page = 1
        items_per_page = 10
        pages = math.ceil(len(friends_data) / items_per_page)
        start = (page - 1) * items_per_page
        end = start + items_per_page
        for index, data in enumerate(friends_data[start:end], start=start):
            name = data["username"]
            total = data["leaderboard"]["total"]
            highScore = data["highScore"]
            gamesPlayed = data["gamesPlayed"]
            winCount = data["winCount"]
            name = f"{'0' if index+1 < 10 else ''}{index+1}. {name}"
            value = f"Total Winnings : {total}\nHigh Score : {highScore}\nGames Won : {winCount}/{gamesPlayed}"
            embed.add_field(name=name, value=value, inline = False)
        pages = 1 if pages == 0 else pages
        embed.set_footer(text=f"Page : {'0' if page < 10 else ''}{page}/{'0' if pages < 10 else ''}{pages}")
        embed.set_thumbnail(url = self.client.user.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        if pages in [0, 1]:
            return await message.edit(embed = embed)
        else:
            if page == 1:
                await message.edit(embed = embed, components=first_page_buttons)
                embed.clear_fields()
        def check(interaction):
            return interaction.message == message
        while True:
            try:
                interaction = await self.client.wait_for('button_click', check=check, timeout=60.0)
            except:
                buttons = await peginator_button(client = self.client, disabled_1 = True, disabled_2 = True, disabled_3 = True, disabled_4 = True)
                return await message.edit(components = buttons)
            
            if interaction.custom_id == "button4":
                page = pages
            elif interaction.custom_id == "button3":
                page += 1
                if page > pages: page = pages
            elif interaction.custom_id == "button2":
                page -= 1
                if page <= 0: page = 1
            else:
                page = 1
                
            start = (page - 1) * items_per_page
            end = start + items_per_page
            for index, data in enumerate(friends_data[start:end], start=start):
                name = data["username"]
                total = data["leaderboard"]["total"]
                highScore = data["highScore"]
                gamesPlayed = data["gamesPlayed"]
                winCount = data["winCount"]
                name = f"{'0' if index+1 < 10 else ''}{index+1}. {name}"
                value = f"Total Winnings : {total}\nHigh Score : {highScore}\nGames Won : {winCount}/{gamesPlayed}"
                embed.add_field(name=name, value=value, inline = False)
            embed.set_footer(text=f"Page : {'0' if page < 10 else ''}{page}/{'0' if pages < 10 else ''}{pages}")
            embed.timestamp = datetime.datetime.utcnow()
            if page == 1:
                await interaction.respond(type = 7, embed=embed, components=first_page_buttons)
            elif page == pages:
                await interaction.respond(type = 7, embed=embed, components=last_page_buttons)
            else:
                await interaction.respond(type = 7, embed=embed, components=middle_page_buttons)
            embed.clear_fields()

    @commands.command()
    async def addfriend(self, ctx, username=None, name=None):
        """Send friend request."""
        if not username or not name:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}addfriend [username] [friend's username]` to send a friend request.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        check_if_exist = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()})
        if check_if_exist:
            try:
                api = HQApi(db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()}).get("access_token"))
                data = await api.search(name)
                id = data["data"][0]["userId"]
            except ApiResponseError:
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            try:
                data = await api.add_friend(id)
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
        check_if_exist = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()})
        if check_if_exist:
            try:
                api = HQApi(db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()}).get("access_token"))
                data = await api.search(name)
                id = data["data"][0]["userId"]
            except ApiResponseError:
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            try:
                data = await api.accept_friend(id)
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
        check_if_exist = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()})
        if check_if_exist:
            try:
                api = HQApi(db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()}).get("access_token"))
                data = await api.search(name)
                id = data["data"][0]["userId"]
            except ApiResponseError:
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            try:
                data = await api.remove_friend(id)
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
        check_if_exist = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()})
        if check_if_exist:
            try:
                api = HQApi(db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()}).get("access_token"))
                data = await api.search(name)
                id = data["data"][0]["userId"]
            except ApiResponseError:
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            data = await api.friend_status(id)
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
