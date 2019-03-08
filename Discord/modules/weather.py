from discord.ext import commands

class Weather():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def weather(self, zipCode : int):
        """Retrieves the weather for a given zip code."""
        await self.bot.say('Not implemented yet.')