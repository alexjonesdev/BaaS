from discord.ext import commands

class Math():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, left : int, right : int):
        """Adds two numbers together."""
        await self.bot.say(left + right)

    @commands.command()
    async def sub(self, left : int, right : int):
        """Subtracts two numbers."""
        await self.bot.say(left - right)

    @commands.command()
    async def mul(self, left : int, right : int):
        """Multiplies two numbers together."""
        await self.bot.say(left * right)

    @commands.command()
    async def div(self, left : int, right : int):
        """Divides two numbers."""
        await self.bot.say(left / right)