#---==IMPORTS==---
from discord.ext import commands

#---==COMMANDS==---
class text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command() #Maybe a timed announcement instead?
    # async def repeat(self, ctx, times : int, content='repeating...'):
    #     """Repeats a message multiple times."""
    #     for i in range(times):
    #         await ctx.send(content)

    @commands.command()
    async def quote(self, ctx, member, searchString):
        """Saves or searches for a quote."""
        await ctx.send('Not implemented yet.')

    @commands.command()
    async def respect(self, ctx):
        """Pays respects."""
        await ctx.send('''FFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFF
FFFFFF
FFFFFF
FFFFFF
FFFFFF
FFFFFF
FFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFF
FFFFFF
FFFFFF
FFFFFF
FFFFFF
FFFFFF
FFFFFF''')

    @commands.command()
    async def mimic(self, ctx, message):
        """Says back what you say."""
        await ctx.send(message)