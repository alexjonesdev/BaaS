from discord.ext import commands

class Math():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, left : float, right : float):
        """Adds two numbers together."""
        await self.bot.say(left + right)

    @commands.command()
    async def sub(self, left : float, right : float):
        """Subtracts two numbers."""
        await self.bot.say(left - right)

    @commands.command()
    async def mul(self, left : float, right : float):
        """Multiplies two numbers together."""
        await self.bot.say(round(left * right), 2)

    @commands.command()
    async def div(self, left : float, right : float):
        """Divides two numbers."""
        await self.bot.say(round(left / right), 2)