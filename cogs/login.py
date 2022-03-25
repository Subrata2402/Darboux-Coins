import discord, random, re
from discord.ext import commands
from HQApi import HQApi
from HQApi.exceptions import ApiResponseError
from database import db

class Login(commands.Cog, HQApi):

    def __init__(self, client):
        super().__init__()
        self.client = client

    async def rand(self):
        ran = random.randint(3,12)
        x = "1234567890"
        uname = ""
        for i in range(ran):
            first = random.choice(("Aingge", "Alhiz", "tanhis", "jabnis", "Hamgish", "jsvjks", "Dayvid", "sognia", "Amyg", "Andya", "Aryda", "Aydun", "Bfhay", "Cgkia", "laidsre", "Clfjor", "Corfja", "Coruco", "Daruwn", "Flefjur", "Evfha", "Ettgja", "Eryrin", "Rotjbin", "Dagjn","Cafhmil","Rintugo","Cfhayli","Difhgna","Efgmma","Gghalen","Helgjma","Jancgje","Grefhtl","Hazgjel","Gwven","Helgen","Ellha","Ehdie",'Igjvy'))
            second = random.choice(("Jill", "Joss", "Juno", "Kady", "Kai", "Kira", "Klara", "germni", "haba", "janis", "Lana", "Leda", "Liesl", "Lily", "Amaa", "Mae", "Lula", "Lucia", "Mia", "Myra", "Opal", "Paige", "Rain", "Quinn", "Rose", "Sia", "Taya", "Teva", "markus", "Judie", "Zuri", "Zoe", "Vera", "Una", "Reeve",'Ekta'))
        c = random.choice(("1", "2", "3"))
        if c == "1":uname = first + second
        elif c == "2":uname = first.title() + second.title()
        elif c == "3": uname = first + second.title()
        d = random.choice(x)
        e = random.choice(x)
        name = uname+d+e
        check = await self.check_username(name)
        if not check:
            return name
        else:
            return await self.rand()

    @commands.command(pass_context=True)
    async def add(self, ctx, number:str=None):
        """Add account using number and OTP."""
        if number is None:
            embed=discord.Embed(title="⚠️ Invalid Argument", description=f"You didn't write number after `{ctx.prefix}add`. Please correct use Command.\n`{ctx.prefix}add +<country code><number>`\nExample: `{ctx.prefix}add +13158686534`", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        try:
            await ctx.message.delete()
        except:
            pass
        def replace(term):
            if len(term.group(0)) == 12:  # UserID
                return term.group(0)[:4]+ '*****' + term.group(0)[-3:]
            elif len(term.group(0)) == 11:  # Mobile
                return term.group(0)[:4]+ '****' + term.group(0)[-3:]
            elif len(term.group(0)) == 13:  # Mobile
                return term.group(0)[:4]+ '******' + term.group(0)[-3:]
            else:
                return term.group(0)
        s_hide = re.sub('\d+', replace, number)
        commander_id = ctx.message.author.id
        try:
            verification = await self.send_code("+" + number, "sms")
            embed=discord.Embed(title="OTP Sent ✅", description=f"Successfully a 6-digits OTP has been sent to your number `{s_hide}` via SMS.\nEnter the OTP within 180 seconds.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            x = await ctx.send(embed=embed)
        except:
            embed=discord.Embed(title="⚠️ Exception Error", description="This is not a valid mobile number or some error occured while adding your account! Please try again later.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        def check(m):
            return m.author == ctx.message.author and m.channel == ctx.message.channel
        try:
            response = await self.client.wait_for('message',check= check, timeout=180)
        except asyncio.TimeoutError:
            em = discord.Embed(title="⚠️ Time Out Error", description="Session timed out, you didn't enter the OTP in time. If you want to login then restart this session once again.", color=discord.Colour.random())
            em.set_thumbnail(url=self.client.user.avatar_url)
            em.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await x.edit(embed=em)
        try:
            code = int(response.clean_content)
            sub_code_res = await self.confirm_code(verification["verificationId"], code)
            name = await self.rand()
            while True:
                try:
                    data = await self.register(verification["verificationId"], name)
                    break
                except Exception as e:
                    await x.edit(content=e)
            access_token = data["accessToken"]
            login_token = data["loginToken"]
            username = data["username"]
            id = data["userId"]
            check = db.profile_base.find_one({"user_id": id})
            if check:
                embed=discord.Embed(title="⚠️ Already Exists", description="This account already exists in bot database. You can't add it again.", color=discord.Colour.random())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
                return await x.edit(embed=embed)
            number_dict = {'id': commander_id,
                           'login_token': login_token,
                           'access_token': a_token,
                           'username': username.lower(),
                           'user_id': id,
                           'auto_play': False,
            }
            db.profile_base.insert_one(number_dict)
            hide_name = "****" + username[4:]
            embed=discord.Embed(title="Account Added ✅", description=f"Successfully linked an account with name `{hide_name}`. Check your DM for more details!", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await x.edit(embed=embed)
            embed=discord.Embed(description=f"Hey {ctx.author.name} you have successfully linked an account with name `{username}` Use `+dcplay {username}` to play HQ Trivia Daily Challenge. For more details use `+help`", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await ctx.author.send(embed=embed)
            channel = self.client.get_channel(841489971109560321)
            await channel.send(f"**{ctx.author}** add an account via number and OTP.")
        except:
            em = discord.Embed(title="❎ Incorrect Code", description="Entered code is incorrect. If you want to login then restart this session once again.", color=discord.Colour.random())
            em.set_thumbnail(url=self.client.user.avatar_url)
            em.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            await x.edit(embed=em)
        

    @commands.command()
    async def remove(self, ctx, username:str):
        """Remove account from database."""
        commander_id = ctx.author.id
        check_id = db.profile_base.find_one({"id": commander_id, "username": username.lower()})
        if not check_id:
            embed=discord.Embed(title="❎ Not Found", description=f"No account found with name `{username}`. Use Command `{ctx.prefix}accounts` to check your all accounts.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)
        db.profile_base.delete_one({"id": ctx.author.id, "username": username.lower()})
        embed=discord.Embed(title="Account Removed", description=f"Successfully removed an account from bot database with name `{username}`", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)
        channel = self.client.get_channel(841490289134796810)
        await channel.send(f"{ctx.author} removed a account from bot database.")

    @commands.command()
    async def removeall(self, ctx):
        """Remove all accounts from database."""
        commander_id = ctx.author.id
        check_id = db.profile_base.find_one({"id": commander_id})
        if not check_id:
            embed=discord.Embed(title="❎ Not Found", description=f"You have not added any accounts. Use Command `{ctx.prefix}add +(country code)(number)` or `{ctx.prefix}addtoken (token)` or `{ctx.prefix}fblogin (fbtoken)` to save your account in bot database and make unlimited coins with bot.", color=discord.Colour.random())
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
            return await ctx.send(embed=embed)

        embed=discord.Embed(description=f"Are you sure you want to remove your all accounts from bot database? Reply with `Yes` within 60 seconds to confirm.", color=0x00ffff)
        x = await ctx.send(embed=embed)

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "yes"
        try:
            message = await self.client.wait_for('message', timeout=60, check=check)
        except:
            embed=discord.Embed(description=f"You have run out of time to reply.", color=0x00ffff)
            return await x.edit(embed=embed)
        id_list = list(db.profile_base.find({"id": commander_id}))
        for id in id_list:
            db.profile_base.delete_one({"id": commander_id})
        embed=discord.Embed(title="Account Removed", description=f"You have successfully removed your all accounts from bot database.", color=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)
        channel = self.client.get_channel(841490289134796810)
        await channel.send(f"{ctx.author} removed all accounts from bot database.")


def setup(client):
    client.add_cog(Login(client))
