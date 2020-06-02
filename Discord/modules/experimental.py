#---==IMPORTS==---
from discord.ext import commands

#---==COMMANDS==---
class experimental(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rooturl = 'https://prnt.sc/'
        self.cur_img_name = 'sqplt8'
        self.minval = 48
        self.maxval = 122
        self.banned_chars = [':',';','<','=','>','?','@','[','\\',']','^','_','`']

    def get_valid_char(self, charVal, sign='down'):
        """Rounds to the nearest valid character value. Wraps back around if the value exceeds min/max limitations."""
        if charVal < self.minval:
            return self.maxval
        elif charVal > self.maxval:
            return self.minval

        newChar = charVal

        if chr(charVal) in self.banned_chars:
            if sign == 'down':
                newChar = self.get_valid_char(charVal - 1,'down')
            else:
                newChar = self.get_valid_char(charVal + 1, 'up')
        
        return newChar

    def calcString(self, curstr, step, index=1):
        """Transforms a string by altering it's character value by the given amount"""
        if step == 0: #Break if there is nothing to do
            return curstr

        newstr = list(curstr)

        if ord(curstr[-index]) + step < self.minval: #Character value is below minimum
            newstr = list(self.calcString(''.join(newstr), -1, index + 1))
            newstr[-index] = chr(self.maxval)
            newstep = self.minval - (ord(curstr[-index]) + step + 1)
            newstr = self.calcString(''.join(newstr), -newstep, index)
        elif ord(curstr[-index]) + step > self.maxval: #Character value is above maximum
            newstr = list(self.calcString(''.join(newstr), 1, index + 1))
            newstr[-index] = chr(self.minval)
            newstep = (ord(curstr[-index]) + step - 1) - self.maxval
            newstr = self.calcString(''.join(newstr), newstep, index)
        else:
            newstr[-index] = chr(self.get_valid_char(ord(curstr[-index]) + step, 'down' if step < 0 else 'up'))
            newstr = ''.join(newstr)

        return newstr

    @commands.group()
    async def prnt(self, ctx):
        """Executes various prnt.sc related commands. (i.e., !prnt <command> <parameters>)"""
        if ctx.invoked_subcommand is None:
            await ctx.send('Must include a subcommand such as "!prnt next"')

    @prnt.command()
    async def start(self, ctx, name):
        """Sets the starting image name. (e.g., !prnt start sqplt8)"""
        if len(name) != 6:
            await ctx.send('Starting value must be 6 characters long.')
        else:
            self.cur_img_name = name
            await ctx.send(self.rooturl + self.cur_img_name)

    @prnt.command()
    async def next(self, ctx, step=1):
        """Returns the next url X number of characters after the current image name. (e.g., !prnt next <5:optional>)"""
        self.cur_img_name = self.calcString(self.cur_img_name, step)
        await ctx.send(self.rooturl + self.cur_img_name)

    @prnt.command()
    async def prev(self, ctx, step=1):
        """Returns the next url X number of characters before the current image name. (e.g., !prnt prev <5:optional>)"""
        self.cur_img_name = self.calcString(self.cur_img_name, step * -1)
        await ctx.send(self.rooturl + self.cur_img_name)