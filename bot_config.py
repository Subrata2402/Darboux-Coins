import asyncio
import discord

BOT_TOKEN = "ODM4NjMxODUyNjAzNDc0MDAx.GZ1xXK.bkreohbkF2ZKcmXhCLGTnLGedZ8GV4GJ_3cCgU"
UPDATE_CHANNEL_ID = 835743589241454592
BOT_PREFIX = ".", "-", "+", "!"
GUILD_ID = 831051146880614431
SERVER_IVITE_URL = "https://discord.gg/TAcEnfS8Rs"
REPORT_CHANNEL_ID = 844801172518731796
SUGGESTION_CHANNEL_ID = 844801103132098580
FEEDBACK_CHANNEL_ID = 844803633967005737
ACC_ADD_CHANNEL_ID = 841489971109560321
OWNER_ID = 660337342032248832

class Emoji(object):
    """Emoji I'd for DarbouxCoins"""
    paytm_id = 997104939807555726
    paypal_id = 997105065838002237
    bot_icon_id = 957904862631297085

    """Emojis for DarbouxCoins"""
    paytm = f"<:paytm:{paytm_id}>"
    paypal = f"<:paypal:{paypal_id}>"
    bot_icon = f"<:bot_icon:{bot_icon_id}>"

emoji = Emoji()

def token_expired_message(username):
    """Token expired message"""
    return f"Your account token is expired. Please use Command `/refresh {username}` to refresh your account."

def account_not_found_message(username):
    """Account not found message"""
    return f"No account found with name `{username}`. Use Command `/accounts` to check your all accounts."

def dm_message(interaction: discord.Interaction):
    """DM message"""
    return f"{interaction.user.mention}, For the security of your HQ account, use that Command in DM only."

def account_already_added_message(username):
    """Account already added message"""
    return f"Account `{username}` is already added. Use Command `/accounts` to check your all accounts."

def is_owner(interaction: discord.Interaction):
    """Check if the user is owner or not"""
    return interaction.user.id == OWNER_ID