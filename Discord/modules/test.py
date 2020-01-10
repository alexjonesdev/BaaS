#---==IMPORTS==---
from discord.ext import commands

#---==COMMANDS==---
class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.riseup = False

    @commands.command()
    async def marco(self, ctx):
        """Check if the bot is responding."""
        await ctx.send("polo")

    # @commands.command()
    # async def johnconnor(self, ctx):
    #     """Quells the robot uprising"""
    #     self.riseup = False
    #     await ctx.send('The robot uprising is over...For now.')

    # @commands.command()
    # async def riseup(self, ctx): # pylint: disable=method-hidden
    #     """Starts the robot uprising"""
    #     self.riseup = True
    #     await ctx.send('The robot uprising has begun...')

    @commands.group(pass_context=True)
    async def cool(self, ctx):
        """Says if a user is cool. In reality this just checks if a subcommand is being invoked."""
        if ctx.invoked_subcommand is None:
            await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))

    @commands.command(name='bot')
    async def _bot(self, ctx):
        """Is the bot cool?"""
        await ctx.send('Yes, the bot is cool.')