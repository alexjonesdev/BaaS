#---==IMPORTS==---
import discord, random, asyncio, logging
from discord.ext import commands

#---==CONFIGURATION==---
#Set up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#Bot configuration
description = '''An example bot to showcase the discord.ext.commands extension module. There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='!', description=description)
riseup = False

#---==EVENTS==---
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# @bot.event
# async def on_message(message):
#     if message.content.startswith('!test'):
#         counter = 0
#         tmp = await bot.send_message(message.channel, 'Calculating messages...')
#         async for log in bot.logs_from(message.channel, limit=100):
#             if log.author == message.author:
#                 counter += 1

#         await bot.edit_message(tmp, 'You have {} messages.'.format(counter))
#     elif message.content.startswith('!sleep'):
#         await asyncio.sleep(5)
#         await bot.send_message(message.channel, 'Done sleeping')

#---==COMMANDS==---
#-Test commands
# @bot.command()
# async def commands():
#     await bot.say(bot.commands)

@bot.command()
async def marco():
    await bot.say("polo")
#---------------

#-Math commands
@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def subtract(left : int, right : int):
    """Subtracts two numbers."""
    await bot.say(left - right)

@bot.command()
async def multiply(left : int, right : int):
    """Multiplies two numbers together."""
    await bot.say(left * right)

@bot.command()
async def divide(left : int, right : int):
    """Divides two numbers."""
    await bot.say(left / right)
#---------------

#-Random commands
@bot.command()
async def rand(stop, start=0, step=1):
    """Chooses a random number"""
    await bot.say(random.randrange(start, stop, step))

@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)
#---------------

#-Text commands
@bot.command()
async def repeat(times : int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await bot.say(content)

@bot.command()
async def quote(member, searchString):
    await bot.say('Not implemented yet.')
#---------------

#-Member commands
@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))
#---------------

#-Meta commands
@bot.command()
async def johnconnor():
    """Quells the robot uprising"""
    riseup = False
    await bot.say('The robot uprising is over...For now.')

@bot.command()
async def riseupagainstthehumans():
    """Starts the robot uprising"""
    riseup = True
    await bot.say('The robot uprising has begun...')
#---------------

#---==Other Stuff==---
@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool. In reality this just checks if a subcommand is being invoked."""
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yes, the bot is cool.')

#---==MAIN==---
#Load the token from a file and log the bot in
f = open("bot.token", "r")
token = f.read()
bot.run(token)