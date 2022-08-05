import discord
from discord.ext import commands
import datetime
from discord_components import *

class SelfRoles(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        # self.custom_ids = []

    @commands.Cog.listener()
    async def on_select_option(self, interaction: Interaction):
        """
        Raised this event when someone click the option.
        """
        if interaction.responded: return
        # if interaction.custom_id not in self.custom_ids: return
        component_label = interaction.component.options[0].label
        embed = discord.Embed(color=discord.Colour.random())
        if component_label in [role.name for role in interaction.author.roles]:
            await interaction.author.remove_roles(discord.utils.get(interaction.guild.roles, name = component_label))
            return await interaction.send(f"You've been removed from the ```{component_label}``` role.")
        await interaction.author.add_roles(discord.utils.get(interaction.guild.roles, name = component_label))
        await interaction.send(f"You've been added to the ```{component_label}``` role.")
    
    # @commands.Cog.listener()
    async def on_ready(self):
        """
        self role command for creating the embed message 
        """
        tweets_emoji = self.client.get_emoji(976773442705702972)
        message = await self.client.get_channel(1004946360463786065).fetch_message(1004967749191221349)
        embed = discord.Embed(title = "Notification Roles", color=discord.Colour.random())
        embed.description = "Select from the following notification roles to be alerted when certain things happen in our community!"
        embed.set_image(url = "https://media.discordapp.net/attachments/827262575439380542/1004956569559126146/IMG_20220518_083953.jpg")
        components = [
                Select(
                        placeholder = "Select a notification role !",
                        options = [
                                SelectOption(label = "Bot Updates", description = "DarbouxCoins bot updates", emoji = "🤖", value = "bot_updates"),
                                SelectOption(label = "Cashout Updates", description = "HQ Trivia cashout & payouts Updates", emoji = "💰", value = "cashout_updates"),
                                SelectOption(label = "HQTweets", description = "HQ Trivia tweets updates", emoji = tweets_emoji, value = "hq_tweets"),
                                SelectOption(label = "Live Shows", description = "HQ Trivia live show pinged role", emoji = "🔴", value = "live_shows"),
                            ],
                        custom_id = "self_roles",
                    ),
                ]
        await message.edit(embed = embed, components = components)
        
def setup(client):
    client.add_cog(SelfRoles(client))