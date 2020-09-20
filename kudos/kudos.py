import discord
from redbot.core import commands, Config
from redbot.core.bot import Red

class Kudos(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.data = Config.get_conf(self, identifier=4386430203532, force_registration=True)
        default_member = {
            "points": 0,
            }
        self.data.register_member(**default_member)

    @commands.group(invoke_without_command=True)
    async def kudos(self, ctx, user: discord.Member, amount: str):
        """Give or check kudos for a user."""
        if ctx.author == user:
            return await ctx.send("You can't give yourself kudos!")

        number_check = await self._int_check(amount)
        data = await self.data.member(user).points()
        if number_check:
            if number_check[0]:
                if number_check[1] == "+":
                    if data is not None:
                        await self.data.member(user).points.set(data+number_check[0])
                        await ctx.send(f"{user.mention}, now has a total of **{data+number_check[0]}** kudos.")
                    if data is None:
                        await self.data.member(user).points.set(number_check[0])
                        await ctx.send(f"{ctx.author.mention}, has given {user.mention} **{data+number_check[0]}** kudos! Good job!")
                elif number_check[1] == "-":
                    if data is None:
                        await self.data.member(user).points.set(0-number_check[0])
                        await ctx.send(f"{ctx.author.mention} has taken {user.mention} **{number_check[0]}** kudos! Thanks!")
                    if data is not None:
                        await self.data.member(user).points.set(data-number_check[0])
                        await ctx.send(f"{user.mention} now has a total of **{data-number_check[0]}** kudos.")
                elif number_check[1] is None:
                    if data is not None:
                        await self.data.member(user).points.set(data+number_check[0])
                        await ctx.send(f"{user.mention}, now has a total of **{data+number_check[0]}** kudos.")
                    if data is None:
                        await self.data.member(user).points.set(number_check[0])
                        await ctx.send(f"{ctx.author.mention}, has given {user.mention} **{data+number_check[0]}** kudos! Good job!")
            elif not number_check:
                return await ctx.send("Invalid number provided!")
        elif not number_check:
            return await ctx.send("Invalid number provided!")

    @kudos.command(name="ranking")
    async def _ranking(self, ctx):
        """View the top 10 users."""
        reps = await self.data.all_members(ctx.guild)
        ranks = sorted(reps, key=lambda x: reps[x]["points"], reverse=True)
        i = 0
        msg = ""
        for x in ranks:
            i = i + 1
            if i > 10:
                break
            user = ctx.guild.get_member(int(x))
            if not user:
                pass
            elif user:
                user_reps = await self.data.member(user).points()
                msg+= f"{i}. `{user}` - {user_reps} kudos\n"
        x=discord.Embed(title="Leaderboard:", description=msg, colour=ctx.author.colour)
        await ctx.send(embed=x)

    @kudos.command(name="check")
    async def _check(self, ctx, user:discord.Member):
        """Checks kudos for a user."""
        data = await self.data.member(user).points()

        if data:
            await ctx.send(f"{user.mention}, has **{data}** kudos.")
        elif not data:
            await ctx.send(f"{user.mention} doesn't have any kudos.")


    async def _int_check(self, amount):
        try:
            if isinstance(int(amount), int):
                return [int(amount), None]
        except ValueError:
            pass

        try:
            if isinstance(int(amount[1:]), int):
                if int(amount[0]) == "+":
                    return [int(amount[1:]), "+"]
                elif int(amount[0]) == "-":
                    return [int(amount[1:]), "-"]
                else:
                    return False
        except ValueError:
            pass

        return False
