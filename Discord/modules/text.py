from discord.ext import commands

class Text:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def repeat(self, times : int, content='repeating...'):
        """Repeats a message multiple times."""
        for i in range(times):
            await self.bot.say(content)

    @commands.command()
    async def quote(self, member, searchString):
        await self.bot.say('Not implemented yet.')