#Scrapes item information from fextralife and imports/updates database entries

#---==IMPORTS==---
import requests, unicodedata, re
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#---==CONFIGURATION==---
engine = create_engine("mysql://discord:AStrongMySQLPassword1!@localhost/discord?charset=utf8mb4") #Make a database engine using whatever you want
great_sword_url = 'https://monsterhunterworld.wiki.fextralife.com/Great+Sword'
sword_shield_url = 'https://monsterhunterworld.wiki.fextralife.com/Sword+&+Shield'
dual_blade_url = 'https://monsterhunterworld.wiki.fextralife.com/Dual+Blades'
long_sword_url = 'https://monsterhunterworld.wiki.fextralife.com/Long+Sword'
hammer_url = 'https://monsterhunterworld.wiki.fextralife.com/Hammer'
hunting_horn_url = 'https://monsterhunterworld.wiki.fextralife.com/Hunting+Horn'
lance_url = 'https://monsterhunterworld.wiki.fextralife.com/Lance'
gunlance_url = 'https://monsterhunterworld.wiki.fextralife.com/Gunlance'
switch_axe_url = 'https://monsterhunterworld.wiki.fextralife.com/Switch+Axe'
charge_blade_url = 'https://monsterhunterworld.wiki.fextralife.com/Charge+Blade'
insect_glaive_url = 'https://monsterhunterworld.wiki.fextralife.com/Insect+Glaive'
bow_url = 'https://monsterhunterworld.wiki.fextralife.com/Bow'
light_bowgun_url = 'https://monsterhunterworld.wiki.fextralife.com/Light+Bowgun'
heavy_bowgun_url = 'https://monsterhunterworld.wiki.fextralife.com/Heavy+Bowgun'
head_armor_url = 'https://monsterhunterworld.wiki.fextralife.com/Master+Rank+Head+Armor'
chest_armor_url = 'https://monsterhunterworld.wiki.fextralife.com/Master+Rank+Chest+Armor'
arm_armor_url = 'https://monsterhunterworld.wiki.fextralife.com/Master+Rank+Arms+Armor'
waist_armor_url = 'https://monsterhunterworld.wiki.fextralife.com/Master+Rank+Waist+Armor'
leg_armor_url = 'https://monsterhunterworld.wiki.fextralife.com/Master+Rank+Leg+Armor'
armor_set_url = 'https://monsterhunterworld.wiki.fextralife.com/Master+Rank+Armor'
charm_url = 'https://monsterhunterworld.wiki.fextralife.com/Charms'
decoration_url = 'https://monsterhunterworld.wiki.fextralife.com/Decorations'
skill_url = 'https://monsterhunterworld.wiki.fextralife.com/Skills'

#---==INITIALIZATION==---
Session = sessionmaker(bind=engine)
base = declarative_base()

#---==CLASSES==---
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
    """Object mapping for mhw_armor table in the database"""
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
    """Object mapping for mhw_armor_set table in the database"""
    __tablename__ = 'mhw_armor_set'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    rarity = Column(Integer)
    bonus = Column(String)
    bonus_description = Column(String)

    def __repr__(self):
        return "<Armor_Set(name='%s', rarity='%d', bonus='%s', bonus_description='%s')>" % (self.name, self.rarity or 0, self.bonus, self.bonus_description)

class Skill(base):
    """Object mapping for mhw_skill table in the database"""
    __tablename__ = 'mhw_skill'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    levels = Column(Integer)

    def __repr__(self):
        return "<Skill(name='%s', description='%s', levels='%d')>" % (self.name, self.description, self.levels or 0)

#---==FUNCTIONS==---
def get_gems(cell):
    """Checks for gem slots on an item and returns the number of each available slot"""
    gem1, gem2, gem3, gem4 = 0, 0, 0, 0
    imgs = cell.find_all('img')

    for img in imgs:
        if img.has_attr('src'):
            if img['src'] == '/file/Monster-Hunter-World/gem_level_1.png':
                gem1 += 1
            elif img['src'] == '/file/Monster-Hunter-World/gem_level_2.png':
                gem2 += 1
            elif img['src'] == '/file/Monster-Hunter-World/gem_level_3.png':
                gem3 += 1
            elif img['src'] == '/file/Monster-Hunter-World/decoration_level_4_mhw_wiki.png':
                gem4 += 1
        elif img.has_attr('title'):
            if img['title'] == 'gem_level_1':
                gem1 += 1
            elif img['title'] == 'gem_level_2':
                gem2 += 1
            elif img['title'] == 'gem_level_3':
                gem3 += 1
            elif img['title'] == 'decoration_level_4_mhw_wiki':
                gem4 += 1
        elif img.has_attr('alt'):
            if img['alt'] == 'gem_level_1':
                gem1 += 1
            elif img['alt'] == 'gem_level_2':
                gem2 += 1
            elif img['alt'] == 'gem_level_3':
                gem3 += 1
            elif img['alt'] == 'decoration_level_4_mhw_wiki':
                gem4 += 1
    return gem1, gem2, gem3, gem4

def get_element(img):
    if img.has_attr('src'):
        if img['src'] == '/file/Monster-Hunter-World/Blastblight.png':
            return 'Blast'
        elif img['src'] == '/file/Monster-Hunter-World/mhw-fire-damage_s.png':
            return 'Fire'
        elif img['src'] == '/file/Monster-Hunter-World/Iceblight.png':
            return 'Ice'
        elif img['src'] == '/file/Monster-Hunter-World/mhw-water-elemental-damage_s.png':
            return 'Water'
        elif img['src'] == '/file/Monster-Hunter-World/paralysis-icon.png':
            return 'Paralysis'
        elif img['src'] == '/file/Monster-Hunter-World/Sleep.png':
            return 'Sleep'
        elif img['src'] == '/file/Monster-Hunter-World/mhw-poison-status-effect-s.png':
            return 'Poison'
        elif img['src'] == '/file/Monster-Hunter-World/thunderblight.png':
            return 'Thunder'
        elif img['src'] == '/file/Monster-Hunter-World/mhw-dragon-damage_s.png':
            return 'Dragon'
    elif img.has_attr('title'):
        if img['title'] == 'Blastblight':
            return 'Blast'
        elif img['title'] == 'mhw-fire-damage_s':
            return 'Fire'
        elif img['title'] == 'Iceblight':
            return 'Ice'
        elif img['title'] == 'mhw-water-elemental-damage_s':
            return 'Water'
        elif img['title'] == 'paralysis-icon':
            return 'Paralysis'
        elif img['title'] == 'Sleep':
            return 'Sleep'
        elif img['title'] == 'mhw-poison-status-effect-s':
            return 'Poison'
        elif img['title'] == 'thunderblight':
            return 'Thunder'
        elif img['title'] == 'mhw-dragon-damage_s':
            return 'Dragon'
    elif img.has_attr('alt'):
        if img['alt'] == 'Blastblight':
            return 'Blast'
        elif img['alt'] == 'mhw-fire-damage_s':
            return 'Fire'
        elif img['alt'] == 'Iceblight':
            return 'Ice'
        elif img['alt'] == 'mhw-water-elemental-damage_s':
            return 'Water'
        elif img['alt'] == 'paralysis-icon':
            return 'Paralysis'
        elif img['alt'] == 'Sleep':
            return 'Sleep'
        elif img['alt'] == 'mhw-poison-status-effect-s':
            return 'Poison'
        elif img['alt'] == 'thunderblight':
            return 'Thunder'
        elif img['alt'] == 'mhw-dragon-damage_s':
            return 'Dragon'

def get_weapons(url, cat):
    """Scrapes the webpage table for basic weapon stats"""
    weapons = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find("table","wiki_table sortable")
    rows = table.tbody.find_all('tr', recursive=False)

    for row in rows:
        cells = row.find_all('td', recursive=False)

        if cat == 'Hammer' and cells[0].a.get_text().strip() == 'Well-Done Hammer': #This entry is incomplete and breaks the scraper
            continue

        gem1, gem2, gem3, gem4 = get_gems(cells[0])
        name = cells[0].a.get_text().replace('n/a', '').strip()
        attack = int(cells[1].get_text().strip())
        affinity = int(cells[2].get_text().strip().split('%')[0])
        rarity = int(cells[4].get_text().strip())
        elem_lock = False
        element_amount = 0
        element_flipped = False
        mod = 0

        if cat == 'Heavy Bowgun':
            mod = int(cells[3].get_text().strip())
            weapons.append(Weapon(category=cat, name=name, attack=attack, affinity=affinity, mod=mod, rarity=rarity, augmentation=0, slot1=gem1, slot2=gem2, slot3=gem3, slot4=gem4))
        else:
            if '(' in cells[3].get_text() or ')' in cells[3].get_text():
                elem_lock = True

            clean_element = re.sub(' {2,}', ' ', cells[3].get_text(' ').replace(u'\xa0', ' ').replace('(', '').replace(')', '').strip())

            no_words = False
            try: #Check if the element cell just has a number and symbol without the element name
                element_amount = int(clean_element)
            except ValueError:
                pass
            else:
                no_words = True

            if no_words == False:
                elem = clean_element.split(' ')
                element = elem[0]

                if elem[0] in ['None','-','--']:
                    element = None
                    element_amount = None
                    elem_lock = None
                elif len(elem) > 3:
                    element = elem[0] + '/' + elem[2]
                    element_amount = elem[1]
                else:
                    element_amount = elem[1]

                try:
                    int(element_amount)
                except ValueError:
                    element_flipped = True
                except TypeError:
                    pass

                if element_flipped == True:
                    weapons.append(Weapon(category=cat, name=name, attack=attack, affinity=affinity, element=element_amount, element_amount=int(element) if element is not None else None, element_locked=elem_lock, rarity=rarity, augmentation=0, slot1=gem1, slot2=gem2, slot3=gem3, slot4=gem4))
                else:
                    weapons.append(Weapon(category=cat, name=name, attack=attack, affinity=affinity, element=element, element_amount=int(element_amount) if element_amount is not None else None, element_locked=elem_lock, rarity=rarity, augmentation=0, slot1=gem1, slot2=gem2, slot3=gem3, slot4=gem4))
            else: #Find the symbol and get the element name from it
                element = get_element(cells[3].img)
                weapons.append(Weapon(category=cat, name=name, attack=attack, affinity=affinity, element=element, element_amount=element_amount, element_locked=elem_lock, rarity=rarity, augmentation=0, slot1=gem1, slot2=gem2, slot3=gem3, slot4=gem4))

    if cat == 'Hammer': #There's a duplicate entry in the hammer table that breaks the insert
        dup = set([i if 'Magda Floga Reforged' == x.name else -1 for i,x in enumerate(weapons)])
        if len(dup) > 2:
            weapons.pop(sorted(dup)[-1])

    return weapons

def get_armor(url, cat):
    """Scrapes the webpage table for basic armor stats"""
    armor = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find("table","wiki_table sortable")
    rows = table.tbody.find_all('tr', recursive=False)

    for row in rows:
        cells = row.find_all('td', recursive=False)
        gem1, gem2, gem3, gem4 = get_gems(cells[4])
        armor.append(Armor(category=cat, name=cells[0].get_text().strip(), rarity=int(cells[1].get_text().strip()), defense=int(cells[3].get_text().strip()), fire=int(cells[5].get_text().strip().replace(" ", "")), water=int(cells[6].get_text().strip().replace(" ", "")), thunder=int(cells[7].get_text().strip().replace(" ", "")), ice=int(cells[8].get_text().strip().replace(" ", "")), dragon=int(cells[9].get_text().strip().replace(" ", "")), slot1=gem1, slot2=gem2, slot3=gem3, slot4=gem4))

    if cat == 'Head': #There's a duplicate entry in the head table that breaks the insert
        dup = set([i if 'Diablos Nero Helm Alpha +' == x.name else -1 for i,x in enumerate(armor)])
        if len(dup) > 2:
            armor.pop(sorted(dup)[-1])

    return armor

def get_armor_sets():
    """Scrapes the webpage for armor sets and any bonus skill they have"""
    armor = []
    response = requests.get(armor_set_url)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find("table","wiki_table sortable")
    rows = table.tbody.find_all('tr', recursive=False)

    for row in rows:
        cells = row.find_all('td', recursive=False)
        bon = cells[9].get_text().strip()
        if bon == 'no bonus' or bon =='--':
            bon = None
        armor.append(Armor_Set(name=cells[1].get_text().replace('Armor Set', '').strip(), rarity=int(cells[0].get_text().strip()), bonus=bon))

    return armor

def get_skills():
    """Scrapes the webpage for skills and their stats"""
    skills = []
    response = requests.get(skill_url)
    soup = BeautifulSoup(response.text, 'lxml')
    headers = soup.find_all('h3', 'titlearea')
    rows = headers[1].find_next_siblings('div', 'row')

    for row in rows:
        cols = row.find_all('div', 'col-sm-3')
        for col in cols:
            cells = col.find_all('p')
            skills.append(Skill(name=unicodedata.normalize('NFKD',cells[0].get_text().strip()), description=unicodedata.normalize('NFKD',cells[1].get_text().strip()), levels=int(unicodedata.normalize('NFKD',cells[2].get_text()).strip().split(' ')[-1].split(':')[-1])))

    return skills

#---==MAIN==---
session = Session()
print('Adding weapons to database...')
print('Adding great sword...')
session.add_all(get_weapons(great_sword_url, 'Great Sword'))
print('Adding sword and shield...')
session.add_all(get_weapons(sword_shield_url, 'Sword & Shield'))
print('Adding dual blade...')
session.add_all(get_weapons(dual_blade_url, 'Dual Blade'))
print('Adding long sword...')
session.add_all(get_weapons(long_sword_url, 'Long Sword'))
print('Adding hammer...')
session.add_all(get_weapons(hammer_url, 'Hammer'))
print('Adding hunting horn...')
session.add_all(get_weapons(hunting_horn_url, 'Hunting Horn'))
print('Adding lance...')
session.add_all(get_weapons(lance_url, 'Lance'))
print('Adding gunlance...')
session.add_all(get_weapons(gunlance_url, 'Gunlance'))
print('Adding switch axe...')
session.add_all(get_weapons(switch_axe_url, 'Switch Axe'))
print('Adding charge blade...')
session.add_all(get_weapons(charge_blade_url, 'Charge Blade'))
print('Adding insect glaive...')
session.add_all(get_weapons(insect_glaive_url, 'Insect Glaive'))
print('Adding bow...')
session.add_all(get_weapons(bow_url, 'Bow'))
print('Adding light bowgun...')
session.add_all(get_weapons(light_bowgun_url, 'Light Bowgun'))
print('Adding heavy bowgun...')
session.add_all(get_weapons(heavy_bowgun_url, 'Heavy Bowgun'))
print('Committing...')
print('Done.')
session.commit()
session.close()

session = Session()
print('Adding armor to database...')
print('Adding head armor...')
session.add_all(get_armor(head_armor_url, 'Head'))
print('Adding chest armor...')
session.add_all(get_armor(chest_armor_url, 'Chest'))
print('Adding arm armor...')
session.add_all(get_armor(arm_armor_url, 'Arm'))
print('Adding waist armor...')
session.add_all(get_armor(waist_armor_url, 'Waist'))
print('Adding leg armor...')
session.add_all(get_armor(leg_armor_url, 'Leg'))
print('Committing...')
print('Done.')
session.commit()
session.close()

session = Session()
print('Adding armor sets to database...')
session.add_all(get_armor_sets())
print('Committing...')
print('Done.')
session.commit()
session.close()

session = Session()
print('Adding skills to database...')
session.add_all(get_skills())
print('Committing...')
print('Done.')
session.commit()
session.close()
