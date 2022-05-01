import discord, aniso8601
from discord.ext import commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from database import db

class Cashout(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def payout(self, ctx, username=None):
        """Get recent payment details."""
        if username is None:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}payout [username]` to check your HQ account cashout details.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        try:
            await ctx.message.delete()
        except:
            pass
        check_if_exist = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()})
        if check_if_exist:
            try:
                api = HQApi(db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()}).get("access_token"))
                data = await api.get_users_me()
            except ApiResponseError:
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please use Command `{ctx.prefix}refresh {username}` to refresh your account.", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            username = data["username"]
            data = await api.get_payouts_me()
            description_info = f""
            for index, data in enumerate(data["payouts"]):
                if index+1 > 10:
                    break
                amount = data["amount"]
                email = data["targetEmail"]
                tim = data["created"]
                tm = aniso8601.parse_datetime(tim).timestamp()
                create_at = f"<t:{int(tm)}>"
                tim = data["modified"]
                tm = aniso8601.parse_datetime(tim).timestamp()
                modify_at = f"<t:{int(tm)}>"
                description_info += f"• Amount :** {amount}**\n• Email :** {email}**\n• Payment Created :** {create_at}**\n• Payment Completed :** {modify_at}**\n\n"
            #await ctx.send("Details send in DM. Please check your DM!")
            embed=discord.Embed(title=f"**__Payout Summary of {username} !__**", description=description_info, color=discord.Colour.random())
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            await ctx.author.send(embed=embed)
            if ctx.guild: await ctx.send(f"{ctx.author.mention}, **Check your DM!**")
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)


    @commands.command()
    async def cashout(self, ctx, email=None, username=None):
        """Make Cashout of an account."""
        if ctx.guild:
            embed=discord.Embed(title="⚠️ Direct Message Only", description="For the security of your HQ account, use that Command in DM only.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        if not email or not username:
            embed=discord.Embed(title="⚠️ Invalid Command", description=f"Use `{ctx.prefix}cashout [email] [username]` to cashout from your HQ Trivia account.", color=discord.Colour.random())
            return await ctx.send(embed=embed)
        check_if_exist = db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()})
        if check_if_exist:
            try:
                api = HQApi(db.profile_base.find_one({"id": ctx.author.id, "username": username.lower()}).get('access_token'))
                data = await api.get_payouts_me()
                bal = data["balance"]
                available = float(bal["available"][1:])
            except ApiResponseError:
                embed=discord.Embed(title="⚠️ Token Expired", description=f"Your account token is expired. Please refresh your account by this command.\n`{ctx.prefix}refresh {username}`", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            if available < float(5):
                need = float(5) - available
                need_money = "{:.2f}".format(need)
                embed=discord.Embed(title="⚠️ Insufficient Balance", description=f"You don't have sufficient balance for cashout. You need more **${need_money}** for cashout.", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await ctx.send(embed=embed)
            try:
                data = await api.make_payout(email)
            except Exception as e:
                embed=discord.Embed(title="⚠️ Api Response Error", description=e, color=discord.Colour.random())
                return await ctx.send(embed=embed)
            data = data["data"]
            amount = data["amount"]
            email = data["targetEmail"]
            embed=discord.Embed(title="**Cashout Done ✅**", description=f"Successfully Cashout of Amount **{amount}** to PayPal Email **{email}**", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)
            channel = self.client.get_channel(841489919067029535)
            await channel.send(f"**{ctx.author}** made a Successfully cashout of amount **{amount}**")
        else:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Cashout(client))
