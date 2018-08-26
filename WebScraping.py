from urllib.request import urlopen
from bs4 import BeautifulSoup
from itertools import chain
import requests


class Player:
    def __init__(self):
        self.name = ""
        self.i_lvl = ""  # item level
        self.n_lvl = ""  # neck level


# ----Getting the characters of rank 3 through Guild Master----
my_url = 'http://eu.battle.net/wow/en/guild/draenor/Ancient_Circle/roster?sort=rank&dir=a'
uClient = urlopen(my_url)
page_html = uClient.read()
uClient.close()
page_soup = BeautifulSoup(page_html, "html.parser")
character_row_1 = page_soup.findAll("tr", {"class": "row1"})
character_row_2 = page_soup.findAll("tr", {"class": "row2"})

l1 = zip(character_row_1, character_row_2)

player_list = []
for char in chain(character_row_1, character_row_2):
    char_container = char.findAll("td", {"class": "rank"})
    rank = char_container[0].text.strip()
    if rank == 'Rank 3' or rank == 'Rank 2' or rank == 'Rank 1' or rank == 'Guild Master':
        name = char.findAll("td", {"class": "name"})
        player_list.append(name[0].text)

raiders = []
for player in player_list:
    url = ('https://www.wowprogress.com/character/eu/draenor/')
    url += player

    uClient = requests.get(url)
    page_html = uClient.text
    uClient.close()

    page_soup = BeautifulSoup(page_html, "html.parser")
    ilvl_container = page_soup.findAll("div", {"class": "gearscore"})
    ilvl = ""
    for div in ilvl_container:
        if "Item Level" in div.text:
            ilvl = div.text.split(" ")[2]

    neck_container = page_soup.findAll("span", {"class": "hint--bottom-right innerLink"})
    neck_lvl = neck_container[0].text
    name = page_soup.title.text.split(" ")[0]

    p = Player()
    p.name = name
    p.i_lvl = ilvl
    p.n_lvl = neck_lvl
    raiders.append(p)

for raider in raiders:
    print(raider.name, "ILVL", raider.i_lvl, "NLVL", raider.n_lvl)
