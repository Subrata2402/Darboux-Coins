import discord, math
from discord.ext import commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
import datetime
from database import db
from discord_components import *
from config.button import peginator_button


class Profile(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def accounts(self, ctx):
        check_id = db.profile_base.find_one({"id": ctx.author.id})
        if not check_id:
            embed=discord.Embed(title="❎ Not Found", description=f"You have not linked any of your accounts in the bot database.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        all_data = list(db.profile_base.find({"id": ctx.author.id}))
        name_list = [data.get("username") for data in all_data]
        name = ""
        api = HQApi()
        for index, username in enumerate(name_list):
            username = (await api.search(username)).get("username")
            name += f"{'0' if index+1 < 10 else ''}{index+1} - {username}\n"
        embed=discord.Embed(title=f"{ctx.author.name}'s accounts !", description = f"```\n{name}\n```", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def profile(self, ctx):
        first_page_buttons = await peginator_button(self.client, disabled_1 = True, disabled_2 = True)
        last_page_buttons = await peginator_button(self.client, disabled_3 = True, disabled_4 = True)
        middle_page_buttons = await peginator_button(self.client)
        
        check_id = db.profile_base.find_one({"id": ctx.author.id})
        if not check_id:
            embed=discord.Embed(title="❎ Not Found", description=f"You have not linked any of your accounts in the bot database.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        if ctx.guild: await ctx.send("Check your DM! Details send in DM's.")
        embed=discord.Embed(title="**Loading Your Accounts...**", color=discord.Colour.random())
        x = await ctx.author.send(embed=embed)
        all_data = list(db.profile_base.find({"id": ctx.author.id}))
        login_token_list = [data.get("login_token") for data in all_data]
        description = ""
        embed=discord.Embed(title="__Available Linked Accounts !__", color=discord.Colour.random())
        page = 1
        items_per_page = 2
        pages = math.ceil(len(login_token_list) / items_per_page)
        start = (page - 1) * items_per_page
        end = start + items_per_page
        for index, login_token in enumerate(login_token_list[start:end], start=start):
            api = HQApi()
            data = await api.get_tokens(login_token)
            name = data["username"]
            user_id = data["userId"]
            access_token = data["accessToken"]
            update = {'access_token': access_token, "username": name.lower()}
            db.profile_base.update_one({"user_id": user_id}, {"$set": update})
            
            api = HQApi(access_token)
            data = await api.get_users_me()
            username = data["username"]
            lives = data["items"]["lives"]
            superSpins = data["items"]["superSpins"]
            erasers = data["items"]["erase1s"]
            coins = data["coins"]
            data = await api.get_payouts_me()
            bal = data["balance"]
            total = bal["prizeTotal"]
            paid = bal["paid"]
            pending = bal["pending"]
            unpaid = bal["unpaid"]
            available = bal["available"]
            unclaimed = bal["frozen"]
            name = f"{'0' if index+1 < 10 else ''}{index+1}. {username}"
            value = f"<:extra_coins:844448578881847326> {coins}\n<:extra_life:844448511264948225> {lives}\n<:eraser:844448550498205736> {erasers}\n💰 {total} (Unclaimed : {unclaimed})\n💸 {available} ready for cashout."
            embed.add_field(name=name, value=value, inline = False)
        pages = 1 if pages == 0 else pages
        embed.set_footer(text=f"Page : {'0' if page < 10 else ''}{page}/{'0' if pages < 10 else ''}{pages}")
        embed.timestamp = datetime.datetime.utcnow()
        if pages in [0, 1]:
            message = await ctx.send(embed = embed)
            return
        else:
            if page == 1:
                message = await ctx.send(embed = embed, components=first_page_buttons)
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
            for index, login_token in enumerate(login_token_list[start:end], start=start):
                api = HQApi()
                data = await api.get_tokens(login_token)
                name = data["username"]
                user_id = data["userId"]
                access_token = data["accessToken"]
                update = {'access_token': access_token, "username": name.lower()}
                db.profile_base.update_one({"user_id": user_id}, {"$set": update})
                
                api = HQApi(access_token)
                data = await api.get_users_me()
                username = data["username"]
                lives = data["items"]["lives"]
                superSpins = data["items"]["superSpins"]
                erasers = data["items"]["erase1s"]
                coins = data["coins"]
                data = await api.get_payouts_me()
                bal = data["balance"]
                total = bal["prizeTotal"]
                paid = bal["paid"]
                pending = bal["pending"]
                unpaid = bal["unpaid"]
                available = bal["available"]
                unclaimed = bal["frozen"]
                name = f"{'0' if index+1 < 10 else ''}{index+1}. {username}"
                value = f"<:extra_coins:844448578881847326> {coins}\n<:extra_life:844448511264948225> {lives}\n<:eraser:844448550498205736> {erasers}\n💰 {total} (Unclaimed : {unclaimed})\n💸 {available} ready for cashout."
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

def setup(client):
    client.add_cog(Profile(client))
