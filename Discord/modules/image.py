#---==IMPORTS==---
from discord.ext import commands

#---==COMMANDS==---
class image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gif(self, ctx, gifName):
        """Returns the gif referenced by name."""
        await ctx.send('Not implemented yet.')