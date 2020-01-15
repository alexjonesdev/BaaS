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
        return "<Weapon(name='%s', category'%s', attack='%d', element='%s', affinity='%d'%%, rarity='%d', gem1 slots='%d', gem2 slots='%d', gem3 slots='%d', augmentations='%d')>" % (self.name, self.category, self.attack or 0, self.element or 0, self.affinity or 0, self.rarity or 0, self.slot1 or 0, self.slot2 or 0, self.slot3 or 0, self.augmentation or 0)


#---==FUNCTIONS==---
def get_gems(cell):
    gem1, gem2, gem3 = 0, 0, 0
    imgs = cell.find_all('img')

    for img in imgs:
        if img['alt'] == 'gem_level_1':
            gem1 += 1
        elif img['alt'] == 'gem_level_2':
            gem2 += 1
        elif img['alt'] == 'gem_level_3':
            gem3 += 1
    return gem1, gem2, gem3

def get_weapons():
    weapons = []
    response = requests.get(great_sword_url)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find("table","wiki_table sortable")
    rows = table.tbody.find_all('tr', recursive=False)

    for row in rows:
        cells = row.find_all('td', recursive=False)
        gem1, gem2, gem3 = get_gems(cells[0])
        weapons.append(Weapon(category='Greatsword', name=cells[0].a.get_text().strip(), attack=int(cells[1].string), affinity=int(cells[2].string.split('%')[0]), element=cells[3].get_text(), rarity=int(cells[4].string), augmentation=0, slot1=gem1, slot2=gem2, slot3=gem3))

    return weapons
#---==MAIN==---