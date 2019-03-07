from discord.ext import commands

class Test:
    def __init__(self, bot):
        self.bot = bot
        self.riseup = False

    @commands.command()
    async def marco(self):
        """Check if the bot is responding."""
        await self.bot.say("polo")

    @commands.command()
    async def johnconnor(self):
        """Quells the robot uprising"""
        self.riseup = False
        await self.bot.say('The robot uprising is over...For now.')

    @commands.command()
    async def riseupagainstthehumans(self):
        """Starts the robot uprising"""
        self.riseup = True
        await self.bot.say('The robot uprising has begun...')

    @commands.group(pass_context=True)
    async def cool(self, ctx):
        """Says if a user is cool. In reality this just checks if a subcommand is being invoked."""
        if ctx.invoked_subcommand is None:
            await self.bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))

    @commands.command(name='bot')
    async def _bot(self):
        """Is the bot cool?"""
        await self.bot.say('Yes, the bot is cool.')