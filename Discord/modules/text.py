from discord.ext import commands

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