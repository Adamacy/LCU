import requests
from bs4 import BeautifulSoup

convert = {
    'The Adaptive Force Shard': 'Adaptive',
    "The Attack Speed Shard": 'AttackSpeed',
    'The Scaling CDR Shard': 'CDRScaling',
    'The Armor Shard': "Armor",
    "The Magic Resist Shard": "MagicRes",
    "The Scaling Bonus Health Shard": "HealthScaling"

}

def getRunes(champion: str):
    """
    Returns dict with best build for selected champion.
    """

    res = requests.get(f'https://u.gg/lol/champions/{champion}/build')
    runes = []
    
    soup = BeautifulSoup(res.text, 'html.parser')

    titles = soup.find_all(class_='perk-style-title')
    primaryRune = titles[0].getText()
    secondaryRune = titles[1].getText()

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


    secondary = soup.find(class_='secondary-tree')
    cos = secondary.find_all(class_='perk-row')

    for i in cos:
        i = i.find(class_='perks')
        i = i.find(class_='perk perk-active')
        if i == None:
            continue
        data = i.find('img')['alt']
        if "The Rune" in data:
            rune = data.replace("The Rune ", "")
            runes.append(rune)

    stats = soup.find(class_='rune-tree_v2 stat-shards-container_v2')
    statsAll = stats.find_all(class_='perks')
    for i in statsAll:
        i = i.find(class_='shard shard-active')
        i = i.find('img')['alt']
        runes.append(convert[i])
    data = {
        "primary": primaryRune,
        "secondary": secondaryRune,
        "ids": runes,
    }
    return data