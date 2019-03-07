import random
from discord.ext import commands

class Random():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rand(self, end : int, begin : int = 0, size : int = 1):
        """Chooses a random number"""
        await self.bot.say(random.randrange(begin, end, size))

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, *choices : str):
        """Chooses between multiple choices."""
        await self.bot.say(random.choice(choices))

    @commands.command()
    async def roll(self, dice : str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.bot.say('Format has to be in NdN!')
            return

        if 1 <= rolls <= 100 and 1 <= limit <= 100:
            result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
            await self.bot.say(result)
        else:
            await self.bot.say('Stop that!')