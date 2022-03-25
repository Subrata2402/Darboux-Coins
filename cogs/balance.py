import discord
from discord.ext import commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from database import db

class Details(commands.Cog, HQApi):

    def __init__(self, client):
        super().__init__()
        self.client = client

    @commands.command(aliases=["bal"])
    async def balance(self, ctx):
        """Get account details."""
        check_id = db.profile_base.find_one({"id": ctx.author.id})
        if not check_id:
            embed=discord.Embed(title="❎ Not Found", description=f"You have not added any of your accounts in bot database.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        if ctx.guild: await ctx.send(f"{ctx.author.mention}, **Check your DM!**")
        embed=discord.Embed(title="Fetching your account balance and Cashout details...", color=0x00ffff)
        x = await ctx.author.send(embed=embed)
        description = ""
        total = paid = pending = unpaid = available = sl_no = ex_no = 0
        token_list = [data.get("access_token") for data in list(db.profile_base.find({"id": ctx.author.id}))]
        for token in token_list:
            try:
                api = HQApi(token)
                data = await api.get_payouts_me()
                bal = data["balance"]
                total = float(total) + float(bal["prizeTotal"][1:])
                paid = float(paid) + float(bal["paid"][1:])
                pending = float(pending) + float(bal["pending"][1:])
                unpaid = float(unpaid) + float(bal["unpaid"][1:])
                available = float(available) + float(bal["available"][1:])
                total = "{:.2f}".format(total)
                paid = "{:.2f}".format(paid)
                pending = "{:.2f}".format(pending)
                unpaid = "{:.2f}".format(unpaid)
                available = "{:.2f}".format(available)
                sl_no = int(sl_no) + 1
                embed=discord.Embed(title=f"**__Balance & Cashout Details of {sl_no} Accounts :__-**", description=f"**• Total Balance :** ${total} 💰\n**• Claimed Ammount :** ${paid} 💸\n**• Pending Ammount :** ${pending} 💰\n**• Unclaimed Ammount :** ${unpaid} 💸\n**• Available for Cashout :** ${available} 💰", color=discord.Colour.random())
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/844442503976583178.gif")
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                await x.edit(embed=embed)
            except:
                ex_no = int(ex_no) + 1
                description += f"{ex_no} - {username}\n"
        embed=discord.Embed(title=f"**__Balance & Cashout Details of {sl_no} Accounts :__-**", description=f"**• Total Balance :** ${total} 💰\n**• Claimed Ammount :** ${paid} 💸\n**• Pending Ammount :** ${pending} 💰\n**• Unclaimed Ammount :** ${unpaid} 💸\n**• Available for Cashout :** ${available} 💰", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await x.edit(embed=embed)
        if ex_no > 0:
            embed=discord.Embed(title="⚠️ Token Expired", description=f"{description}\nThis account's tokens are expired. Please refresh your accounts to use this command `{ctx.prefix}refresh <username>`", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.author.send(embed=embed)

def setup(client):
    client.add_cog(Details(client))
