import discord
from discord.ext import commands

class Member:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joined(self, member : discord.Member):
        """Says when a member joined."""
        if member:
            await self.bot.say('{0.name} joined in {0.joined_at}'.format(member))
        else:
            await self.bot.say('Member not found.')