import codecs

import requests
from bs4 import BeautifulSoup

NAT_OUT_FILE = "dex-0-nat.txt"
REG_OUT_FILE = "dex-1-reg.txt"
COM_OUT_FILE = "dex-2-com.txt"

NAT_DICT = {}

# A set to track the regional pokemon names and disregard duplicates
REG_NAME_LIST = []

def get_nat_dex():
    """Scrapes the national pokedex into a file."""
    with codecs.open(NAT_OUT_FILE, "w", "utf-8") as file:
        # Get the page contents
        url = "https://pokemondb.net/pokedex/national"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        
        # Parsing the html data into rows of [national #, name]
        entries = soup.find_all("span", class_="infocard-lg-data text-muted")
        
        # Getting the national numbers and name.
        i = 0
        for entry in entries:
            i = i + 1
            
            num = entry.find("small").text
            name = entry.find("a", class_="ent-name").text
            
            # IMPORTANT!!! Note that we store the name as the key and the value as the number.
            # We pull only the names from the regional dex and in the combined dex, we pull
            # the number from this dictionary, store as [num, name] in the final list, and then
            # sort it by number before printing it out.
            NAT_DICT[name] = num
            file.write(num + " " + name + "\n")
            
            # Box separation space
            if i % 30 == 0:
                file.write("\n")


def get_reg_dex():
    """Scrapes the regional pokedex(es) into a file."""
    with codecs.open(REG_OUT_FILE, "w", "utf-8") as file:
        urls = [
            "https://pokemondb.net/pokedex/game/sword-shield",
            "https://pokemondb.net/pokedex/game/sword-shield/isle-of-armor",
            "https://pokemondb.net/pokedex/game/sword-shield/crown-tundra"
        ]
        
        for url in urls:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            
            # Getting the table entries
            entries = soup.find_all("span", class_="infocard-lg-data text-muted")
            
            # Getting just the name
            i = 0
            for entry in entries:
                pokemon_name = entry.find("a", class_="ent-name").text
                if pokemon_name not in REG_NAME_LIST:
                    i = i + 1
                    REG_NAME_LIST.append(pokemon_name)
                    file.write(pokemon_name + "\n")

                    # Box separation space
                    if i % 30 == 0:
                        file.write("\n")


def get_com_dex():
    """A custom dex list that orders the regional pokemons by the national numbers."""
    
    out_list = []
    for name in REG_NAME_LIST:
        num = NAT_DICT.get(name)
        out_list.append(num + " " + name)
    
    with codecs.open(COM_OUT_FILE, "w", "utf-8") as file:
        i = 0
        for entry in sorted(out_list):
            i = i + 1
            file.write(entry + "\n")
            
            # Box separation space
            if i % 30 == 0:
                file.write("\n")


get_nat_dex()
get_reg_dex()
get_com_dex()
