import discord
from discord.ext import commands
import datetime
from discord_components import *

class SelfRoles(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.custom_ids = ["cashout_updates", "hq_tweets", "announcement", "bot_updates"]

    @commands.Cog.listener()
    async def on_select_option(self, interaction: Interaction):
        if interaction.responded: return
        # if interaction.custom_id not in self.custom_ids: return
        embed = discord.Embed(color=discord.Colour.random())
        if interaction.component.label in [role.name for role in interaction.author.roles]:
            await interaction.author.remove_roles(interaction.component.label)
            return await interaction.send(f"You've been removed from the ```{interaction.component.label}``` role.")
        await interaction.author.remove_roles(interaction.component.label)
        await interaction.send(f"You've been added to the ```{interaction.component.label}``` role.")
    
    @commands.command(name = "selfrole")
    async def _self_role(self, ctx):
        embed = discord.Embed(title = "Notification Roles", color=discord.Colour.random())
        embed.description = "Select from the following notification roles to be alerted when certain things happen in our community!"
        embed.set_image(url = "https://im.ge/i/FbW2A9")
        components = [
                Select(
                        placeholder = "Select a role...",
                        options = [
                                SelectOption(label = "Bot Updates", description = "DarbouxCoins bot updates", emoji = "🤖", value = "bot_updates"),
                                SelectOption(label = "Cashout Updates", description = "HQ Trivia cashout & payouts Updates", emoji = "💰", value = "cashout_updates"),
                            ],
                        custom_id = "self_roles",
                    ),
        await ctx.send(embed = embed, components = components)