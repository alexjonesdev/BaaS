from discord.ext import commands

class Image:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gif(self, gifName):
        """Returns the gif referenced by name."""
        await self.bot.say('Not implemented yet.')