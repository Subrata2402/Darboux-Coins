import discord, aniso8601
from discord.ext import commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from database import db

class Details(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def details(self, ctx, username=None):
        """Get account details."""
        if username is None:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}details [username]` to check your HQ Trivia account details.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        check_id = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()})
        if check_id:
            embed = discord.Embed(title = "Loading your account details...", color = discord.Colour.random())
            message = await ctx.author.send(embed = embed)
            if ctx.guild: await ctx.send("Check your DM! Details send in DM's.")
            try:
                api = HQApi(db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()}).get("access_token"))
                data = await api.get_users_me()
            except ApiResponseError as e:
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await message.edit(embed=embed)
            coins = data.get("coins") if data.get("coins") else 0
            payout_data = await api.get_payouts_me()
            balance_data = payout_data['balance']
            unclaimed = balance_data['frozen']
            auto_play_mode = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()}).get("auto_play")
            embed = discord.Embed(title = f"**__Statistics of HQ Account !__**",
                description = f"**• Username :** {data['username']}\n" \
                    f"**• Mobile Number :** {data['phoneNumber']}\n" \
                    f"**• Auto-play Mode :** {'Enable' if auto_play_mode else 'Disable'}\n"
                    f"**• Blocked :** {data['blocksMe']}",
                color = discord.Colour.random())
            embed.add_field(name = f"🔥 __PowerUps Details :__-", inline = False,
                value = f"**• Total Coins :** {coins} <:extra_coins:844448578881847326>\n" \
                    f"**• Total Lives :** {data['items']['lives']} <:extra_life:844448511264948225>\n" \
                    f"**• Super Spins :** {data['items']['superSpins']} <:super_spin:844448472908300299>\n" \
                    f"**• Total Erasers :** {data['erase1s']} <:eraser:844448550498205736>"
                )
            embed.add_field(name = "💸 __Balance & Cashout Details :__-", inline = False,
                value = f"**• Total Balance :** {balance_data['prizeTotal']} 💰\n" \
                    f"**• Claimed Ammount :** {balance_data['paid']} 💸\n" \
                    f"**• Pending Ammount :** {balance_data['pending']} 💰\n" \
                    f"**• Unclaimed Ammount :** {balance_data['unpaid']} 💸\n" \
                    f"**• Available for Cashout :** {balance_data['available']} 💰"
                )
            embed.add_field(name = "🔴 __Live Games Details :__-", inline = False,
                value = f"**• Games Won :** {data['leaderboard']['alltime']['wins']}/{data['gamesPlayed']}\n" \
                    f"**• High Score :** {data['highScore']}\n" \
                    f"**• Rank :** {'None' if data['leaderboard']['rank'] == 101 else data['leaderboard']['rank']}\n"
                )
            embed.set_footer(text = f"ID: {data['userId']} | Created At")
            embed.timestamp = aniso8601.parse_datetime(data['created'])
            embed.set_thumbnail(url = data['avatarUrl'])
            await message.edit(embed = embed)
        else:
            embed = discord.Embed(title = ":negative_squared_cross_mark: Not Found", description = f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color = discord.Colour.random())
            embed.set_thumbnail(url = self.client.user.avatar_url)
            embed.set_footer(text = self.client.user, icon_url = self.client.user.avatar_url)
            await ctx.send(embed = embed)

    
def setup(client):
    client.add_cog(Details(client))
