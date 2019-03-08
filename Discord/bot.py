#---==IMPORTS==---
import logging #discord, asyncio,
from discord.ext import commands
from modules import test, math, weather, text, random, member, image

#---==CONFIGURATION==---
#Set up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#Bot configuration
description = '''A bot service made from the discord.py library. Commands:'''
bot = commands.Bot(command_prefix='!', description=description)

#Load modules
bot.add_cog(test.Test(bot))
bot.add_cog(math.Math(bot))
bot.add_cog(random.Random(bot))
bot.add_cog(text.Text(bot))
bot.add_cog(member.Member(bot))

#---==EVENTS==---
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#---==COMMANDS==---

#---==MAIN==---
#Load the token from a file and log the bot in
f = open("bot.token", "r")
token = f.read()
bot.run(token)