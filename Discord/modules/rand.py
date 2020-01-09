import random
from discord.ext import commands

class rand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rand(self, ctx, end : int, begin : int = 0, size : int = 1):
        """Chooses a random number."""
        await ctx.send(random.randrange(begin, end, size))

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, *choices : str):
        """Chooses between multiple choices."""
        await ctx.send(random.choice(choices))

    @commands.command()
    async def flip(self, ctx):
        """Flips a coin."""
        await ctx.send(random.choice(['Heads','Tails']))

    @commands.command()
    async def roll(self, ctx, dice : str = '1d100'):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        if 1 <= rolls <= 100 and 1 <= limit <= 100:
            result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
            await ctx.send(result)
        else:
            await ctx.send('Stop that!')