#---==IMPORTS==---
from discord.ext import commands
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#---==CONFIGURATION==---
engine = create_engine("mysql://discord:AStrongMySQLPassword1!@localhost/discord?charset=utf8mb4") #Make a database engine using whatever you want

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
    affinity = Column(Integer)
    slot1 = Column(Integer)
    slot2 = Column(Integer)
    slot3 = Column(Integer)
    augmentation = Column(Integer)
    
    def __repr__(self):
        return "<Weapon(name='%s', category'%s', attack='%d', element='%s', affinity='%d', gem lvl1 slots='%d', gem lvl2 slots='%d', gem lvl3 slots='%d', augmentations='%d')>" % (self.name, self.category, self.attack, self.element, self.affinity, self.slot1, self.slot2, self.slot3, self.augmentation)

class Armor(base):
    __tablename__ = 'mhw_armor'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    rarity = Column(Integer)
    defense = Column(Integer)
    fire = Column(Integer)
    water = Column(Integer)
    thunder = Column(Integer)
    ice = Column(Integer)
    dragon = Column(Integer)
    slot1 = Column(Integer)
    slot2 = Column(Integer)
    slot3 = Column(Integer)
    slot4 = Column(Integer)

    def __repr__(self):
        return "<Armor(name='%s', category='%s', rarity='%d', defense='%d', fire='%d', water='%d', thunder='%d', ice='%d', dragon='%d', gem1 slots='%d', gem2 slots='%d', gem3 slots='%d', gem4 slots='%d')>" % (self.name, self.category, self.rarity or 0, self.defense or 0, self.fire or 0, self.water or 0, self.thunder or 0, self.ice or 0, self.dragon or 0, self.slot1 or 0, self.slot2 or 0, self.slot3 or 0, self.slot4 or 0)

class Skill(base):
    __tablename__ = 'mhw_skill'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    levels = Column(Integer)

    def __repr__(self):
        return "<Skill(name='%s', description='%s', levels='%d')>" % (self.name, self.description, self.levels or 0)

#---==COMMANDS==---
class mhw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def mhw(self, ctx):
        """Executes various MHW related commands (i.e., !mhw <command> <search phrase>)"""
        if ctx.invoked_subcommand is None:
            await ctx.send('Must include a subcommand such as "!mhw weapon"')

    @mhw.command()
    async def weapon(self, ctx, *, name):
        """Returns the stats of a weapon (e.g., !mhw weapon Iron Bow I) """
        sess = Session()
        wep = sess.query(Weapon).filter(Weapon.name.like('%'+ name + '%')).first()
        sess.close()
        if wep == None:
            await ctx.send('Weapon not found.')
        else:
            await ctx.send(wep)

    @mhw.command()
    async def armor(self, ctx, *, name):
        """Returns the stats of an armor piece (e.g. !mhw armor Odogaron)"""
        sess = Session()
        ar = sess.query(Armor).filter(Armor.name.like('%'+ name + '%')).first()
        sess.close()
        if ar == None:
            await ctx.send('Armor not found.')
        else:
            await ctx.send(ar)

    @mhw.command()
    async def skill(self, ctx, *, name):
        """Returns the description & max level of a skill (e.g. !mhw skill attack)"""
        sess = Session()
        ar = sess.query(Skill).filter(Skill.name.like('%'+ name + '%')).first()
        sess.close()
        if ar == None:
            await ctx.send('Skill not found.')
        else:
            await ctx.send(ar)

    @mhw.command()
    async def monster(self, ctx, *, name):
        """Returns the stats of a monster (e.g., !mhw monster Great Jagras)"""
        await ctx.send('Not implemented yet.')
