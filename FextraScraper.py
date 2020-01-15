#Scrapes item information from fextralife and imports/updates database entries

#---==IMPORTS==---
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, DateTime
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

#---==INITIALIZATION==---
Session = sessionmaker(bind=engine)
base = declarative_base()

#---==CLASSES==---
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
    rarity = Column(Integer)

    def __repr__(self):
        return "<Weapon(name='%s', category='%s', attack='%d', element='%s', affinity='%d'%%, rarity='%d', gem1 slots='%d', gem2 slots='%d', gem3 slots='%d', augmentations='%d')>" % (self.name, self.category, self.attack or 0, self.element or 0, self.affinity or 0, self.rarity or 0, self.slot1 or 0, self.slot2 or 0, self.slot3 or 0, self.augmentation or 0)


#---==FUNCTIONS==---
def get_gems(cell):
    gem1, gem2, gem3 = 0, 0, 0
    imgs = cell.find_all('img')

    for img in imgs:
        if img.has_attr('alt'):
            if img['alt'] == 'gem_level_1':
                gem1 += 1
            elif img['alt'] == 'gem_level_2':
                gem2 += 1
            elif img['alt'] == 'gem_level_3':
                gem3 += 1
    return gem1, gem2, gem3

def get_weapons(url, cat):
    weapons = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find("table","wiki_table sortable")
    rows = table.tbody.find_all('tr', recursive=False)

    for row in rows:
        cells = row.find_all('td', recursive=False)
        gem1, gem2, gem3 = get_gems(cells[0])
        weapons.append(Weapon(category=cat, name=cells[0].a.get_text().strip(), attack=int(cells[1].string), affinity=int(cells[2].string.split('%')[0]), element=cells[3].get_text(), rarity=int(cells[4].string), augmentation=0, slot1=gem1, slot2=gem2, slot3=gem3))

    if cat == 'Hammer': #There's a duplicate entry in the hammer table that breaks the insert
        weps = set([i if 'Magda Floga Reforged' == x.name else -1 for i,x in enumerate(weapons)])
        if len(weps) > 2:
            weapons.pop(sorted(weps)[-1])

    return weapons

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
session.add_all(get_weapons(light_bowgun_url, 'Heavy Bowgun'))
print('Adding heavy bowgun...')
session.add_all(get_weapons(heavy_bowgun_url, 'Light Bowgun'))
print('Committing...')
print('Done.')
session.commit()
session.close()