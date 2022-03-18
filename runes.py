import requests
from bs4 import BeautifulSoup


def getRunes(champion: str):
    res = requests.get(f'https://u.gg/lol/champions/{champion}/build')

    runes = []
    
    soup = BeautifulSoup(res.text, 'html.parser')

    title = soup.find(class_='perk-style-title').get_text()
    primary = soup.find(class_='rune-tree_v2 primary-tree')
    primary = primary.find(class_='perk keystone perk-active')

    primary = primary.find_all('img')[0]['alt']
    
    if "The Keystone" in primary:
        runes.append(primary.replace("The Keystone ", ""))

    rune = soup.find(class_='rune-tree_v2 primary-tree')
    rune = rune.find_all(class_='perk-row')

    for i in rune:
        i = i.find(class_='perks')
        i = i.find(class_='perk perk-active')
        if i == None:
            continue
        data = i.find('img')['alt']
        if "The Rune" in data:
            rune = data.replace("The Rune ", "")
            runes.append(rune)


    secondary = soup.find(class_='rune-tree_v2 secondary-tree')
    secondary = secondary.find()
    data = {
        'primary': (title, runes),
        'secondary': ('secondTitle', 'Runes')
    }
    return data

print(getRunes('Shaco'))