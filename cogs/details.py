import discord
from discord.ext import commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from database import db

class Details(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def details(self, ctx, username=None):
        """Get account details."""
        if username is None:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}details [username]` to check your HQ Trivia account details.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
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
            username = data["username"]
            id = data["userId"]
            avatar_url = data["avatarUrl"]
            upt = data["created"]
            uptm = aniso8601.parse_datetime(upt)
            uptim = uptm.astimezone(timezone("Asia/Kolkata"))
            created_at = uptim.strftime("%b %d, %Y %I:%M %p")
            ph_no = data["phoneNumber"]
            lives = data["items"]["lives"]
            superSpins = data["items"]["superSpins"]
            erasers = data["items"]["erase1s"]
            coins = data["coins"]
            api = HQApi(token)
            data = api.get_payouts_me()
            bal = data["balance"]
            total = bal["prizeTotal"]
            paid = bal["paid"]
            pending = bal["pending"]
            unpaid = bal["unpaid"]
            available = bal["available"]
            unclaimed = bal["frozen"]
            
            embed=discord.Embed(title=f"**__Statistics of HQ Account !__**", description=f"**Username: `{username}`\nMobile Number: `{ph_no}`**", color=discord.Colour.random())
            embed.add_field(name=f"**🔥 __Items(Lives, Spin, Erasers, Coins)__**", value=f"**• Total Coins :** {coins} <:extra_coins:844448578881847326>\n**• Total Lives :** {lives} <:extra_life:844448511264948225>\n**• Super Spins :** {superSpins} <:super_spin:844448472908300299>\n**• Total Erasers :** {erasers} <:eraser:844448550498205736>")
            embed.add_field(name="**💸 __Balance & Cashout Details :__-**", value=f"**• Total Balance :** {total} 💰\n**• Claimed Ammount :** {paid} 💸\n**• Pending Ammount :** {pending} 💰\n**• Unclaimed Ammount :** {unpaid} 💸\n**• Available for Cashout :** {available} 💰")
            embed.set_footer(text=f"ID: {id} | Created At: {created_at}")
            embed.set_thumbnail(url=avatar_url)
            await ctx.author.send(embed=embed)
            if ctx.guild: await ctx.send("Check your DM! Details send in DM's.")
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=0x00ffff)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)

    
def setup(client):
    client.add_cog(Details(client))
