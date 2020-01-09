#---==IMPORTS==---
import logging, logging.config #discord, asyncio,
from discord.ext import commands
from modules import test, math, weather, text, rand, member, image

#---==CONFIGURATION==---
description = '''A bot service made from the discord.py library. Commands:'''
command_prefix = '!'
logging_config = 'logging.conf'
primary_logger = 'discord'

#---==INITIALIZATION==---
#Set up logging
logging.config.fileConfig(logging_config)
logger = logging.getLogger(primary_logger)

#Set up the bot
bot = commands.Bot(command_prefix=command_prefix, description=description)

#Load modules
logger.info('Loading modules...')
bot.add_cog(test.test(bot))
logger.info('MODULE LOADED: test')
bot.add_cog(math.math(bot))
logger.info('MODULE LOADED: math')
bot.add_cog(rand.rand(bot))
logger.info('MODULE LOADED: random')
bot.add_cog(text.text(bot))
logger.info('MODULE LOADED: text')
bot.add_cog(member.member(bot))
logger.info('MODULE LOADED: Member')
logger.info('Modules loaded.')

#---==EVENTS==---
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    logger.info('Bot has logged in as %s:%s', bot.user.name, bot.user.id)

#---==COMMANDS==---
@bot.command()
async def ping(ctx):
    """Pings the bot."""
    logger.info('Received !ping command')
    await ctx.send('pong')
    logger.info('Responded with "pong"')

#---==MAIN==---
#Load the token from a file and log the bot in
f = open("bot.token", "r")
token = f.read()
f.close()
bot.run(token)