import requests
from bs4 import BeautifulSoup

URL = "https://pokemondb.net/pokedex/game/sword-shield/crown-tundra"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

# Getting the table entries
entries = soup.find_all("span", class_="infocard-lg-data text-muted")

# Getting just the name
for entry in entries:
    pokemon_name = entry.find("a", class_="ent-name")
    print(pokemon_name.text)
