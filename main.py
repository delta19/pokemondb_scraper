import codecs

import requests
from bs4 import BeautifulSoup

OUT_FILE = "galar-dex.txt"

# Opening a file to write to
with codecs.open(OUT_FILE, "w", "utf-8") as file:
    urls = [
        "https://pokemondb.net/pokedex/game/sword-shield",
        "https://pokemondb.net/pokedex/game/sword-shield/isle-of-armor",
        "https://pokemondb.net/pokedex/game/sword-shield/crown-tundra"
    ]
    
    # A set to track names and make sure no duplicates are printed
    name_set = set()
    
    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        
        # Getting the table entries
        entries = soup.find_all("span", class_="infocard-lg-data text-muted")
        
        # Getting just the name
        for entry in entries:
            pokemon_name = entry.find("a", class_="ent-name").text
            if pokemon_name not in name_set:
                name_set.add(pokemon_name)
                file.write(pokemon_name + "\n")
