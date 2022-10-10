import sys
import traceback
import discord, aniso8601
from discord.ext import commands
from discord import app_commands
from HQApi import HQApi
import bot_config

class Show(commands.Cog, HQApi):

    def __init__(self, client: commands.Bot):
        super().__init__()
        self.client = client

    @app_commands.command(name="nextshow", description="Get HQ Trivia next show details.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def _next_show_details(self, interaction: discord.Interaction):
        """Get HQ next show details."""
        await interaction.response.defer()
        response_data = await self.get_show()
        tim = (response_data["nextShowTime"])
        tm = aniso8601.parse_datetime(tim).timestamp()
        time = f"<t:{int(tm)}>"
        prize = (response_data["nextShowPrize"])
        for data in response_data["upcoming"]:
            type = data["nextShowLabel"]["title"]
        embed=discord.Embed(title="**__HQ Next Show Details !__**", description=f"**• Show Name : {type}\n• Show Time : {time}\n• Prize Money : {prize}**", color=discord.Colour.random())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/799237115962851348/816261537101905951/1200px-HQ_logo.svg.png")
        await interaction.followup.send(embed=embed)

    @_next_show_details.error
    async def _app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """Error handler for app commands"""
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"This command is on cooldown. Try again in **{round(error.retry_after, 2)}** seconds.", ephemeral=True)
        elif isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("The command execution is failed for some conditions are not satisfied. ", ephemeral=True)
        else:
            print(f"Error loading {interaction.command} command!", file=sys.stderr)
            traceback.print_exc()


async def setup(client: commands.Bot):
    await client.add_cog(Show(client))