# import discord
from discord.ext import commands

class member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    # @commands.command()
    # async def joined(self, ctx, member : discord.Member):
    #     """Says when a member joined."""
    #     if member:
    #         await self.bot.say('{0.name} joined in {0.joined_at}'.format(member))
    #     else:
    #         await self.bot.say('Member not found.')