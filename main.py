from base64 import b64encode
import requests
import json
import asyncio
from exceptions import Errors
from bs4 import BeautifulSoup
import runes
from subprocess import check_output

exceptions = Errors()

convert = {
    'The Adaptive Force Shard': 'Adaptive',
    "The Attack Speed Shard": 'AttackSpeed',
    'The Scaling CDR Shard': 'CDRScaling',
    'The Armor Shard': "Armor",
    "The Magic Resist Shard": "MagicRes",
    "The Scaling Bonus Health Shard": "HealthScaling"
}

style = {
    'Domination': 8100,
    'Inspiration': 8300,
    'Precision': 8000,
    'Resolve': 8400,
    'Sorcery': 8200
}

class Api:

    lang = 'en_US'
    champion = None
    autoImport = False

    def __init__(self) -> None:

        #self.data = check_output('wmic PROCESS WHERE "name=\'LeagueClientUx.exe\'" GET commandline')
        #"--app-port=50680"
        self.data = open('D:/Riot Games/League of Legends/lockfile').read().split(':')
        #print(self.data.decode('utf-8').split('--app-port=')[1].split('"')[0])
        self.certificate = 'cer.pem'
        self.uri = 'https://127.0.0.1'
        try:
            self.port = self.data[2]
            self.password = self.data[3]
        except:
            raise exceptions.gameNotStarted()
        self.endpoint = None
        self.data = None
        auth = f'riot:{self.password}'.encode('ascii')
        self.headers = {
            'Authorization': f"Basic {b64encode(auth).decode('ascii')}",
            'Content-type': 'application/json'
        }

    def get(self, endpoint: str, data: dict = {}):
        try:
            self.conn = requests.get(f'{self.uri}:{self.port}{endpoint}',
                                     verify=self.certificate, headers=self.headers, data=data)
            return self.conn
        except ConnectionError:
            raise exceptions.gameNotStarted()

    def post(self, endpoint: str, data={}):
        self.conn = requests.post(f'{self.uri}:{self.port}{endpoint}',
                                  verify=self.certificate, headers=self.headers, data=data)
        return self.conn

    def put(self, endpoint: str, data={}):
        self.conn = requests.put(f'{self.uri}:{self.port}{endpoint}',
                                 verify=self.certificate, headers=self.headers, data=data)
        return self.conn

    def delete(self, endpoint: str, data={}):
        self.conn = requests.delete(
            f'{self.uri}:{self.port}{endpoint}', verify=self.certificate, headers=self.headers, data=data)
        return self.conn

    def patch(self, endpoint: str, data={}):
        self.conn = requests.patch(f'{self.uri}:{self.port}{endpoint}',
                                   verify=self.certificate, headers=self.headers, data=data)
        return self.conn

    def getLangauges(self):
        lang = requests.get(
            'https://ddragon.leagueoflegends.com/cdn/languages.json').json()
        return lang

    def setLanguage(self, lang: str):
        if lang in self.getLangauges():
            pass
        else:
            raise exceptions.languageWrongValue()
        self.lang = lang

    def setChampion(self, champion: str):
        self.champion = champion.capitalize()
        if champion not in self.getAllChampions():
            raise exceptions.championWrongName()
        else:
            self.champion = champion

    def getPlayersPicks(self):
        """Return array of champions name selected during champion select"""
        session = self.get('/lol-champ-select/v1/session').json()
        summoner = self.get('/lol-summoner/v1/current-summoner').json()
        champions = []
        
        self.puuid = summoner['puuid']
        self.summonerID = summoner['summonerId']
        self.accountID = summoner['accountId']
        try:
            if session['httpStatus'] == 404:
                return exceptions.matchNotFound()
        except KeyError:
            for i in session['actions'][0]:
                if i['type'] == 'ban':
                    continue
                championID = i['championId']
                if championID == 0:
                    pass
                else:
                    champ = self.get(
                        f'/lol-champions/v1/inventories/{self.summonerID}/champions/{championID}')
                    champions.append(champ.json()['name'])
                    for x in session['myTeam']:
                        if summoner['summonerId'] == x['summonerId']:
                            if self.autoImport == True:
                                if x['championId'] == 0:
                                    pass
                                else:
                                    champ = self.get(f"/lol-champions/v1/inventories/{self.summonerID}/champions/{x['championId']}")
                                    self.setChampion(champ.json()['name'])
                                    self.importRunes()
            return champions

    def getAllChampions(self):

        champions = requests.get(
            'http://ddragon.leagueoflegends.com/cdn/12.5.1/data/en_US/champion.json')

        return list(champions.json()['data'].keys())

    def getChampStats(self):
        if self.lang == None:
            raise exceptions.languageNotSet()
        if self.champion not in self.getAllChampions():
            raise exceptions.championWrongName()
        info = requests.get(
            f'http://ddragon.leagueoflegends.com/cdn/12.5.1/data/{self.lang}/champion/{self.champion}.json')

        return info.json()

    def getCounters(self):

        res = requests.get(
            f'http://www.lolcounter.com/champions/{self.champion}', headers={'User-Agent': "counter-lol"})
        soup = BeautifulSoup(res.text, 'html.parser')
        counters = soup.find(class_='weak-block')

        counters = counters.find_all(class_="champ-block")
        counter_list = [counter.find(class_='name').get_text()
                        for counter in counters]

        return counter_list

    def getChampionImage(self):
        """Returns champion image as bytes"""


        data = self.getChampStats()['data'][self.champion]
        i = data['image']['full']
        return f'http://ddragon.leagueoflegends.com/cdn/12.5.1/img/champion/{i}'

    def getChampionSpells(self):
        """Returns an array of champion spells and passive"""

        data = self.getChampStats()['data'][self.champion]
        self.spellNames = []
        for spell in data['spells']:
            self.spellNames.append(spell['name'])
        self.spellNames.append(data['passive']['name'])

        return self.spellNames

    def getSpellsImage(self):
        """Return images of all champion spells"""
        data = self.getChampStats()['data'][self.champion]
        images = []
        for i in data['spells']:
            i = i['image']['full']
            spellImage = f'http://ddragon.leagueoflegends.com/cdn/12.5.1/img/spell/{i}'
            images.append(spellImage)

        passive = f"http://ddragon.leagueoflegends.com/cdn/12.5.1/img/passive/{data['passive']['image']['full']}"
        images.append(passive)

        return images

    def allRunes(self):
        return self.get('/lol-perks/v1/perks').json()

    def getChampBuild(self):
        """
        Returns dict with best build for selected champion.
        """

        res = requests.get(f'https://u.gg/lol/champions/{self.champion}/build')
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
        runesIds = json.loads(open('./runes.json', 'r').read())
        runesConverted = []
        for i in runes:
            runesConverted.append(runesIds[i])

        data = {
            "primary": style[primaryRune],
            "secondary": style[secondaryRune],
            "ids": runesConverted,
        }
        
        return data

    def importRunes(self):
        
        runes = self.getChampBuild()
        id = self.get('/lol-perks/v1/currentpage').json()['id']
        self.delete(f'/lol-perks/v1/pages/{id}')
        data = {
            "autoModifiedSelections": [
                0
            ],
            "current": True,
            "id": 0,
            "isActive": True,
            "isDeletable": True,
            "isEditable": True,
            "isValid": True,
            "lastModified": 0,
            "name": f"{self.champion} build",
            "order": 0,
            "primaryStyleId": 0,
            "selectedPerkIds": [],
            "subStyleId": 0
        }
        data['primaryStyleId'] = runes['primary']
        data['subStyleId'] = runes['secondary']
        data['selectedPerkIds'] = runes['ids']

        self.post('/lol-perks/v1/pages', data=json.dumps(data))
        return data