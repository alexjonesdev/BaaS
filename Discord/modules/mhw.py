#---==IMPORTS==---
from discord.ext import commands
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

#---==CONFIGURATION==---
engine = create_engine("mysql://discord:AStrongMySQLPassword1!@localhost/discord?charset=utf8mb4") #Make a database engine using whatever you want

#---==INITIALIZATION==---
Session = sessionmaker(bind=engine)
base = declarative_base()
emojis = {  "defense":"<:defense:667736167705346048>", "fire":"<:fire:667736167642300426>", "water":"<:water:667736167336116226>",
            "thunder":"<:thunder:667736167709540392>", "ice":"<:ice:667736167600619532>", "dragon":"<:dragon:667736167671791626>",
            "gem1":"<:gem1:667736167520927744>", "gem2":"<:gem2:667736167671922688>", "gem3":"<:gem3:667736167739031582>",
            "gem4":"<:gem4:667736167436910632>", "ammo":"<:ammo:669574033829920768>", "greatsword":"<:greatsword:669573349327765542>",
            "hammer":"<:hammer:669574016163381258>", "affinity":"<:affinity:672171533845921792>", "blast":"<:blast:672181061869895686>",
            "sleep":"<:sleep:672181062226542593>", "poison":"<:poison:672181062201507851>", "paralysis":"<:paralysis:672181062247645194>"}

#---==DATABASE==---
class Test(base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    value = Column(String)
    
    def __repr__(self):
        return "<Test(id='%d', value='%s')>" % (self.id, self.value)

class Weapon(base):
    """Object mapping for mhw_weapon table in the database"""
    __tablename__ = 'mhw_weapon'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    attack = Column(Integer)
    element = Column(String)
    element_amount = Column(Integer)
    element_locked = Column(Boolean)
    mod = Column(Integer)
    affinity = Column(Integer)
    slot1 = Column(Integer)
    slot2 = Column(Integer)
    slot3 = Column(Integer)
    slot4 = Column(Integer)
    augmentation = Column(Integer)
    rarity = Column(Integer)

    def __repr__(self):
        return "<Weapon(name='%s', category='%s', attack='%d', element='%s', amount='%d', locked='%s', mods='%d', affinity='%d'%%, rarity='%d', gem1 slots='%d', gem2 slots='%d', gem3 slots='%d', gem4 slots='%d', augmentations='%d')>" % (self.name, self.category, self.attack or 0, self.element, self.element_amount or 0, str(self.element_locked), self.mod or 0, self.affinity or 0, self.rarity or 0, self.slot1 or 0, self.slot2 or 0, self.slot3 or 0, self.slot4 or 0, self.augmentation or 0)

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

class Armor_Set(base):
    __tablename__ = 'mhw_armor_set'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    rarity = Column(Integer)
    bonus = Column(String)
    bonus_description = Column(String)
    pieces = relationship("Armor_Set_Piece")

    def __repr__(self):
        return "<Armor_Set(name='%s', rarity='%d', bonus='%s', bonus_description='%s')>" % (self.name, self.rarity or 0, self.bonus, self.bonus_description)

class Armor_Set_Piece(base):
    __tablename__ = 'mhw_armor_set_piece'
    id = Column(Integer, primary_key=True)
    armor_set_id = Column(Integer, ForeignKey('mhw_armor_set.id'))
    armor_id = Column(Integer, ForeignKey('mhw_armor.id'))
    armor = relationship("Armor")

    def __repr__(self):
        return "<Armor_Set_Piece(id='%d', set_id='%d', armor_id='%d')>" % (self.id or -1, self.armor_set_id or -1, self.armor_id or -1)

class Skill(base):
    __tablename__ = 'mhw_skill'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    levels = Column(Integer)

    def __repr__(self):
        return "<Skill(name='%s', description='%s', levels='%d')>" % (self.name, self.description, self.levels or 0)

#---==FUNCTIONS==---
def get_attack_emote(category):
    """Returns the emote for a given weapon category."""
    if category in ['Bow', 'Heavy Bowgun', 'Light Bowgun']:
        return emojis['ammo']
    elif category in ['Hammer', 'Hunting Horn']:
        return emojis['hammer']
    elif category in ['Charge Blade', 'Dual Blade', 'Great Sword', 'Gunlance', 'Insect Glaive', 'Lance', 'Long Sword', 'Switch Axe', 'Sword & Shield']:
        return emojis['greatsword']
    else:
        return 'Attack:'

def get_element_emote(element):
    """Returns the emote for a given element"""
    if '/' in element:
        element_pieces = element.split('/')
        return get_element_emote(element_pieces[0]) + '/' + get_element_emote(element_pieces[1])
    elif element == 'Fire':
        return emojis['fire']
    elif element == 'Water':
        return emojis['water']
    elif element == 'Ice':
        return emojis['ice']
    elif element == 'Thunder':
        return emojis['thunder']
    elif element == 'Dragon':
        return emojis['dragon']
    elif element == 'Blast':
        return emojis['blast']
    elif element == 'Paralysis':
        return emojis['paralysis']
    elif element == 'Sleep':
        return emojis['sleep']
    elif element == 'Poison':
        return emojis['poison']
    else:
        return ''

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
            response = '''**{0}**:  R{1}
{2}{3},   ({4}{5}),   {6}{7},
{8}{9},   {10}{11},   {12}{13}   {14}{15}'''.format(wep.name, wep.rarity,
get_attack_emote(wep.category), wep.attack, get_element_emote(wep.element), wep.element_amount, emojis['affinity'], wep.affinity,
emojis['gem1'], wep.slot1, emojis['gem2'], wep.slot2, emojis['gem3'], wep.slot3, emojis['gem4'], wep.slot4)
            await ctx.send(response if wep.element_locked == True else response.replace('(', '').replace(')', ''))

    @mhw.command()
    async def armor(self, ctx, *, name):
        """Returns the stats of an armor piece (e.g. !mhw armor Odogaron)"""
        sess = Session()
        ar = sess.query(Armor).filter(Armor.name.like('%'+ name + '%')).first()
        sess.close()
        if ar == None:
            await ctx.send('Armor not found.')
        else:
            await ctx.send('''**{0}**:  R{1}
{2}{3},   {4}{5},   {6}{7},   {8}{9},   {10}{11},   {12}{13}
{14}{15},   {16}{17},   {18}{19},   {20}{21}'''.format(ar.name, ar.rarity,
emojis['defense'], ar.defense, emojis['fire'], ar.fire, emojis['water'], ar.water, emojis['thunder'], ar.thunder, emojis['ice'], ar.ice, emojis['dragon'], ar.dragon,
emojis['gem1'], ar.slot1, emojis['gem2'], ar.slot2, emojis['gem3'], ar.slot3, emojis['gem4'], ar.slot4))

    @mhw.command()
    async def set(self, ctx, *, name):
        """Returns the stats of a weapon (e.g., !mhw weapon Iron Bow I) """
        sess = Session()
        ar = sess.query(Armor_Set).filter(Armor_Set.name.like('%'+ name + '%')).first()
        sess.close()
        if ar == None:
            await ctx.send('Armor set not found.')
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
