import discord
from discord.ext import commands

class 


async def peginator_button(client: commands.Bot, emojis: list[discord.PartialEmoji], disableds: list[bool]):
    """Peginator button"""
    view = discord.ui.View()
    for i in range(len(emojis)):
        view.add_item(discord.ui.Button(label=emojis[i], disabled=disableds[i], style = discord.ButtonStyle.blue, custom_id = f"button_{i}"))
    
