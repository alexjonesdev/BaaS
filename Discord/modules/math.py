from discord.ext import commands

class math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, left : float, right : float):
        """Adds two numbers together."""
        await ctx.send(left + right)

    @commands.command()
    async def sub(self, ctx, left : float, right : float):
        """Subtracts two numbers."""
        await ctx.send(left - right)

    @commands.command()
    async def mul(self, ctx, left : float, right : float):
        """Multiplies two numbers together."""
        await ctx.send(round(left * right, 2))

    @commands.command()
    async def div(self, ctx, left : float, right : float):
        """Divides two numbers."""
        await ctx.send(round(left / right, 2))