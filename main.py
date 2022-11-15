from base64 import b64encode
import requests
import json
import os
from exceptions import Errors
from bs4 import BeautifulSoup
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

def changeName(i: str):
    print(f"Before change: {i}")

    if i == "Cho'Gath":
        i = "Chogath"
    if i == "Dr. Mundo":
        i = 'DrMundo'
    if i == 'Wukong':
        i = "MonkeyKing"
    if i == "Kog'Maw":
        i = "KogMaw"
    if i == "Cho'Gath":
        i = "Chogath"

    if " " in i:
        i = i.split(" ")
        i = i[0].capitalize() + i[1].capitalize()

    print(f"After change: {i}")

    return i

class LCU:
    """
        Class where you have most of avaiable requests in Riot Api
    """
    lang = 'en_US'
    champion = None
    autoImport = False

    def __init__(self) -> None:
        self.data = check_output(
            'wmic PROCESS WHERE "name=\'LeagueClientUx.exe\'" GET commandline').decode('utf-8')

        self.certificate = 'cer.pem'
        self.uri = f'https://127.0.0.1'
        try:
            self.port = int(self.data.split("--app-port=")
                            [1][0:].split(' ')[0][:-1])
            self.password = self.data.split(
                "--remoting-auth-token=")[1][0:].split(' ')[0][:-1]
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
        """
            Gives all the languages avaiable in the API
        """
        lang = requests.get(
            'https://ddragon.leagueoflegends.com/cdn/languages.json').json()
        return lang

    def setLanguage(self, lang: str):
        """
            Set language you want to get responses
        """
        if lang in self.getLangauges():
            pass
        else:
            raise exceptions.languageWrongValue()
        self.lang = lang

    def setChampion(self, champion: str):
        """
            Function used to set champion for another functions
        """
        self.champion = champion.capitalize()
        if champion not in self.getAllChampions():
            raise exceptions.championWrongName()
        else:
            self.champion = champion

    def getTeammates():
        pass

    def getPlayersPicks(self):
        """
            Return array of champions name selected during champion select
        """
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
                        if summoner['summonerId'] == x['summonerId'] and x['championId'] != 0:
                            champ = self.get(
                                    f"/lol-champions/v1/inventories/{self.summonerID}/champions/{x['championId']}").json()
                            if self.autoImport == True:
                                self.champion = champ['name']
                                self.importRunes()
                        else:
                            champ = None
            return (champions, champ)

    def getAllChampions(self):
        """
            Gives array with all champions in the game
        """
        champions = requests.get(
            'http://ddragon.leagueoflegends.com/cdn/12.5.1/data/en_US/champion.json')

        return list(champions.json()['data'].keys())

    def getChampStats(self):
        """
            Returns data about champion skills
        """

        if self.lang == None:
            raise exceptions.languageNotSet()
        if self.champion not in self.getAllChampions():
            raise exceptions.championWrongName()
        info = requests.get(
            f'http://ddragon.leagueoflegends.com/cdn/12.5.1/data/{self.lang}/champion/{self.champion}.json')

        return info.json()

    def getCounters(self):
        """
            Returns array of champion counters
        """
        counters = []
        res = requests.get(f"https://u.gg/lol/champions/{self.champion}/counter")
        soup = BeautifulSoup(res.text, 'html.parser')

        best_counters = soup.find_all(class_='counter-list-card best-win-rate')
        for i in best_counters:
            name = i.find(class_="champion-name").get_text()
            wr = i.find(class_="win-rate").get_text().split(" ")[0]
            data = {
                "name": name,
                "wr": wr,
            }
            counters.append(data)
        return counters

    def getChampionImage(self):
        """Returns champion image as bytes"""

        data = self.getChampStats()['data'][self.champion]
        i = data['image']['full']
        return f'http://ddragon.leagueoflegends.com/cdn/12.5.1/img/champion/{i}'

    def getChampLoadingScreen(self):
        data = self.get(f"/lol-game-data/assets/ASSETS/Characters/{self.champion}/Skins/Base/{self.champion}LoadScreen.jpg")
        return data

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

    def setChampion(self, champion: str) -> None:
        self.champion = changeName(champion)

        return None

    def getChampData(self):
        stats = requests.get(f"http://ddragon.leagueoflegends.com/cdn/12.21.1/data/en_US/champion/{self.champion}.json").json()
        
        data = {
            "stats": stats,
            "counters": self.getCoutners(),
            "build": self.getChampBuild()
        }


    def allRunes(self):
        """
            Returns all runes avaiable in the game
        """
        return self.get('/lol-perks/v1/perks').json()

    def getChampBuild(self):
        """
        Returns dict with best build for selected champion
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

    def getChampionData(self):
        pass

    def getGameData(self):
        data = self.get("/lol-gameflow/v1/session")
        print(data.json())

    def importRunes(self):
        """
            Importing runes into the game.
        """
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