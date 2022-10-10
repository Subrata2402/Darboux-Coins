import time
import aiohttp
import discord
import bot_config
from discord.ext import commands
from discord import app_commands
import platform


class General(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="stats", description="Get bot stats.")
    @app_commands.check(bot_config.is_owner)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def _check_bot_stats(self, interaction: discord.Interaction):
        """Get Bot Stats."""
        await interaction.response.defer()
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.client.guilds)
        memberCount = len(set(self.client.get_all_members()))
        # channelCount = len(set(self.client.get_all_channels()))
        total_commands = len(self.client.commands)

        embed = discord.Embed(
            description="```\n"
            f"● Bot Latency        ::  {round(self.client.latency * 100)}ms\n"
            f"● Coding Language    ::  Python[{pythonVersion}]\n"
            f"● Library Version    ::  {dpyVersion}\n"
            f"● Bot Version        ::  2.0\n"
            f"● Total Guilds       ::  {serverCount}\n"
            f"● Total Users        ::  {memberCount}\n"
            f"● Total Commands     ::  {total_commands}\n"
            f"● Bot Developer      ::  Subrata#4099 (660337342032248832)\n```",
            color=discord.Colour.random())

        embed.set_footer(text=f"Created At")
        embed.timestamp = self.client.user.created_at
        # embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_author(
            name=f"{self.client.user} | Bot Info !", icon_url=self.client.user.avatar.url)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="say", description="Send message.")
    @app_commands.check(bot_config.is_owner)
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def _say(self, interaction: discord.Interaction, *, message: str):
        """Send Message."""
        await interaction.response.defer()
        await interaction.followup.send(message)

    @app_commands.command(name="ping", description="Get bot latency.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def _ping(self, interaction: discord.Interaction):
        """ Pong! """
        await interaction.response.send_message(content=f"**__Pong!__** :ping_pong:  **{round(self.client.latency * 100)}ms**")

    @app_commands.command(name="uptime", description="Get bot uptime.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def _uptime(self, interaction: discord.Interaction):
        """ Get bot uptime. """
        await interaction.response.send_message(content=f"**__Uptime__** :clock1:  **{self.client.uptime}**")

    @app_commands.command(name="sendmsg", description="Send invite link to user.")
    @app_commands.check(bot_config.is_owner)    
    @app_commands.describe(user = 'User to send message')
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def _send_dm_to_user(self, ctx, user: discord.User) -> None:
        """ Send message to user """
        if not user: return await ctx.send(f"User `{user}` not found!")
        await user.send(user.mention + "  https://discord.gg/TAcEnfS8Rs")
        await ctx.send("DM Successfully send to `{}`!".format(user))

    @app_commands.command(name = "donate", description = "Donate to the bot developer.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def _donate(self, interaction: discord.Interaction):
        """ Donate to the bot developer. """
        paytm_emoji = self.client.get_emoji(bot_config.emoji.paytm_id)
        paypal_emoji = self.client.get_emoji(bot_config.emoji.paypal_id)
        description = f"Maintaining a bot requires a huge amount of time and resources. Your donation will help in the maintenance of the {self.client.user.mention} and always keep me motivated. " \
            f"If you think {self.client.user.mention} helped you in any way, your donation would be a great help.\n\n" \
            f"Please use the buttons below to donate. Thank you."
        embed = discord.Embed(
            title="Donation!", description=description, color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar.url)
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label = "Paytm", style = discord.ButtonStyle.url, url  = "https://paytm.me/x-WGerG", emoji = paytm_emoji))
        view.add_item(discord.ui.Button(label = "Paypal", style = discord.ButtonStyle.url, url  = "https://paypal.me/sakhman", emoji = paypal_emoji))
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="invite", description="Invite the bot to your server.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def _invite(self, interaction: discord.Interaction):
        """ Invite the bot to your server. """
        await interaction.response.send_message("You can't invite the bot to your server.", ephemeral=True)

    @app_commands.command(name="support", description="Join the support server.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def _support(self, interaction: discord.Interaction):
        """ Join the support server. """
        emoji = self.client.get_emoji(bot_config.emoji.bot_icon_id)
        view = discord.ui.View().add_item(discord.ui.Button(label="Click Here to Join", style=discord.ButtonStyle.url, url=bot_config.SERVER_IVITE_URL, emoji=emoji))
        description = f"Need help with {self.client.user.mention}? Join the support server by clicking the button below. " \
            f"Please make sure you read the rules first. Thank you."
        embed = discord.Embed(
            title="Support Server!", description=description, color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar.url)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name = "report", description = "Report a bug or issue.")
    @app_commands.describe(message= "Message to report")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def _report(self, interaction: discord.Interaction, *, message: str):
        """ Report a bug or issue. """
        if not message: return await interaction.response.send_message("Please provide a message to report.", ephemeral=True)
        await interaction.response.defer(ephemeral=True)
        channel = self.client.get_channel(bot_config.REPORT_CHANNEL_ID)
        embed = discord.Embed(
            title="Report!", description=message, color=discord.Colour.random())
        embed.set_footer(text=f"User ID: {interaction.user.id}")
        embed.set_author(
            name=f"{interaction.user}", icon_url=interaction.user.avatar.url)
        embed.set_thumbnail(url=interaction.user.avatar.url)
        embed.timestamp = discord.utils.utcnow()
        await channel.send(embed=embed)
        await interaction.followup.send("Your report has been sent to the developer. Thank you.", ephemeral=True)

    @app_commands.command(name="reply", description="Reply to a user.")
    @app_commands.check(bot_config.is_owner)
    @app_commands.describe(user = 'User to reply', message = 'Message to reply')
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def _reply(self, interaction: discord.Interaction, user: discord.User, *, message: str):
        """ Reply to a user. """
        if not user: return await interaction.response.send_message("User not found!", ephemeral=True)
        if not message: return await interaction.response.send_message("Please provide a message to reply.", ephemeral=True)
        await interaction.response.defer(ephemeral=True)
        try:
            await user.send(message)
            await interaction.followup.send(f"Message successfully send to `{user}`!", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("I can't send message to this user.", ephemeral=True)

    @app_commands.command(name="eval", description="Evaluate python code.")
    @app_commands.check(bot_config.is_owner)
    @app_commands.describe(code = 'Code to evaluate')
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def _eval(self, interaction: discord.Interaction, *, code: str):
        """ Evaluate python code. """
        if not code: return await interaction.response.send_message("Please provide code to evaluate.", ephemeral=True)
        await interaction.response.defer(ephemeral=True)
        try:
            t1 = time.perf_counter()
            result = eval(code)
            t2 = time.perf_counter()
            if result is None:
                result = "None"
            else:
                result = str(result)
            await interaction.followup.send(f"**Result:**\n```{result}```\n**Time Taken:** `{round(t2 - t1, 4)}` seconds", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"**Error:**\n```{e}```", ephemeral=True)


    @app_commands.command(name="suggest", description="Suggest a feature.")
    @app_commands.describe(message = 'Message to suggest')
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def _suggest(self, interaction: discord.Interaction, *, message: str):
        """ Suggest a feature. """
        if not message: return await interaction.response.send_message("Please provide a message to suggest.", ephemeral=True)
        await interaction.response.defer(ephemeral=True)
        channel = self.client.get_channel(bot_config.SUGGESTION_CHANNEL_ID)
        embed = discord.Embed(
            title="Suggestion!", description=message, color=discord.Colour.random())
        embed.set_footer(text=f"User ID: {interaction.user.id}")
        embed.set_author(
            name=f"{interaction.user}", icon_url=interaction.user.avatar.url)
        embed.set_thumbnail(url=interaction.user.avatar.url)
        embed.timestamp = discord.utils.utcnow()
        msg = await channel.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        await interaction.followup.send("Your suggestion has been sent to the developer. Thank you.", ephemeral=True)

    @app_commands.command(name="feedback", description="Give feedback.")
    @app_commands.describe(message = 'Message to give feedback')
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def _feedback(self, interaction: discord.Interaction, *, message: str):
        """ Give feedback. """
        if not message: return await interaction.response.send_message("Please provide a message to give feedback.", ephemeral=True)
        await interaction.response.defer(ephemeral=True)
        channel = self.client.get_channel(bot_config.FEEDBACK_CHANNEL_ID)
        embed = discord.Embed(
            title="Feedback!", description=message, color=discord.Colour.random())
        embed.set_footer(text=f"User ID: {interaction.user.id}")
        embed.set_author(
            name=f"{interaction.user}", icon_url=interaction.user.avatar.url)
        embed.set_thumbnail(url=interaction.user.avatar.url)
        embed.timestamp = discord.utils.utcnow()
        await channel.send(embed=embed)
        await interaction.followup.send("Your feedback has been sent to the developer. Thank you.", ephemeral=True)

    @app_commands.command(name="hqname", description="Get HQ name of a user.")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def _hqname(self, interaction: discord.Interaction):
        """Get HQ Random US Name."""
        url = "https://randomuser.me/api/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                name = data["results"][0]["name"]["first"]
                await interaction.response.send_message(name)

    # @_eval.error
    # @_reply.error
    # @_send_dm_to_user.error
    # @_check_bot_stats.error
    # @_feedback.error
    # @_suggest.error
    # @_report.error
    # @_support.error
    # @_invite.error
    # @_ping.error
    # @_uptime.error
    # @_donate.error
    # @_hqname.error
    @commands.Cog.listener()
    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"This command is on cooldown. Try again in **{round(error.retry_after, 2)}** seconds.", ephemeral=True)
        elif isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("The command execution is failed for some conditions are not satisfied.", ephemeral=True)
    

async def setup(client: commands.Bot):
    await client.add_cog(General(client))
                        #  guilds=[discord.Object(id=bot_config.GUILD_ID)])