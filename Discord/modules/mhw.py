#---==IMPORTS==---
from discord.ext import commands
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#---==CONFIGURATION==---
engine = create_engine("mysql://user:password@localhost/discord?charset=utf8") #Make a database engine using whatever you want

#---==INITIALIZATION==---
Session = sessionmaker(bind=engine)
base = declarative_base()

#---==DATABASE==---
class Test(base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    value = Column(String)
    
    def __repr__(self):
        return "<Test(id='%d', value='%s')>" % (self.id, self.value)

class Weapon(base):
    __tablename__ = 'mhw_weapon'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    attack = Column(Integer)
    element = Column(String)
    slot1 = Column(Integer)
    slot2 = Column(Integer)
    slot3 = Column(Integer)
    augmentation = Column(Integer)
    
    def __repr__(self):
        return "<Weapon(name='%s', category'%s', attack='%d', element='%s', gem lvl1 slots='%d', gem lvl2 slots='%d', gem lvl3 slots='%d', augmentations='%d')>" % (self.name, self.category, self.attack, self.element, self.slot1, self.slot2, self.slot3, self.augmentation)

#---==COMMANDS==---
class mhw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def mhw(self, ctx):
        """Executes various MHW related commands"""
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid mhw command passed...')

    @mhw.command()
    async def weapon(self, ctx, *, name):
        """Returns the stats of a weapon"""
        sess = Session()
        mytest = sess.query(Weapon).filter(Weapon.name == name).first()
        sess.close()
        await ctx.send(mytest)

    @commands.command()
    async def mhwdb(self, ctx, id=1):
        """Test DB function"""
        sess = Session()
        mytest = sess.query(Test).get(id)
        sess.close()
        await ctx.send(mytest)