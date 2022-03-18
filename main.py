from base64 import b64encode
import requests
import json
import asyncio
from exceptions import Errors
from bs4 import BeautifulSoup

exceptions = Errors()


class Api:

    lang = None

    def __init__(self) -> None:

        file = open(
            '/home/adam/Games/league-of-legends/drive_c/Riot Games/League of Legends/lockfile', 'r')
        self.data = file.read().split(':')
        self.certificate = 'cer.pem'
        self.uri = 'https://127.0.0.1'
        self.port = self.data[2]
        self.password = self.data[3]
        self.endpoint = None
        self.data = None

        auth = f'riot:{self.password}'.encode('ascii')
        self.headers = {
            'Authorization': f"Basic {b64encode(auth).decode('ascii')}",
            'Content-type': 'application/json'
        }

    def get(self, endpoint: str, data: dict = {}):
        self.conn = requests.get(f'{self.uri}:{self.port}{endpoint}',
                                 verify=self.certificate, headers=self.headers, data=data)
        return self.conn

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

    def langauges(self):
        lang = requests.get(
            'https://ddragon.leagueoflegends.com/cdn/languages.json').json()
        return lang

    def setLanguage(self, lang: str):
        if lang in self.langauges():
            pass
        else:
            raise exceptions.languageWrongValue()
        self.lang = lang

    def getPlayersPicks(self):
        """Return array of champions name selected during champion select"""
        session = self.get('/lol-champ-select/v1/session').json()
        summoner = self.get('/lol-summoner/v1/current-summoner').json()
        champions = []

        self.puuid = summoner['puuid']
        self.summonerID = summoner['summonerId']
        self.accountID = summoner['accountId']
        try:
            for i in session['actions'][0]:
                championID = i['championId']
                if championID == 0:
                    pass
                else:
                    champ = self.get(
                        f'/lol-champions/v1/inventories/{self.summonerID}/champions/{championID}')
                    champions.append(champ.json()['name'])
            return champions
        except:
            raise exceptions.matchNotFound()

    def getAllChampions(self):

        champions = requests.get(
            'http://ddragon.leagueoflegends.com/cdn/12.5.1/data/en_US/champion.json')
        return champions.json()

    def getChampStats(self, champion: str):
        if self.lang == None:
            raise exceptions.languageNotSet()
        if champion not in list(self.getAllChampions()['data'].keys()):
            raise exceptions.championWrongName()
        info = requests.get(
            f'http://ddragon.leagueoflegends.com/cdn/12.5.1/data/{self.lang}/champion/{champion}.json')

        return info.json()

    def getCounters(self, champion: str):

        res = requests.get(
            f'http://www.lolcounter.com/champions/{champion}', headers={'User-Agent': "counter-lol"})
        soup = BeautifulSoup(res.text, 'html.parser')
        counters = soup.find(class_='weak-block')

        counters = counters.find_all(class_="champ-block")
        counter_list = [counter.find(class_='name').get_text()
                        for counter in counters]

        return counter_list

    def getChampionImage(self, champion: str):
        """Returns champion image as bytes"""

        champion = champion.capitalize()

        data = self.getChampStats(champion)['data'][champion]
        i = data['image']['full']
        return f'http://ddragon.leagueoflegends.com/cdn/12.5.1/img/champion/{i}'

    def getChampionSpells(self, champion: str):
        """Returns an array of champion spells and passive"""

        data = self.getChampStats(champion)['data'][champion]
        self.spellNames = []
        for spell in data['spells']:
            self.spellNames.append(spell['name'])
        self.spellNames.append(data['passive']['name'])

        return self.spellNames

    def getSpellsImage(self, champion: str):
        """Return images of all champion spells"""
        data = self.getChampStats(champion)['data'][champion]
        images = []
        for i in data['spells']:
            i = i['image']['full']
            spellImage = f'http://ddragon.leagueoflegends.com/cdn/12.5.1/img/spell/{i}'
            images.append(spellImage)

        passive = f"http://ddragon.leagueoflegends.com/cdn/12.5.1/img/passive/{data['passive']['image']['full']}"
        images.append(passive)

        return images

    def getChampionBuild(self, champion: str):
        """Get build for champion"""

        res = requests.get(f'https://u.gg/lol/champions/{champion}/build')

lcu = Api()
lcu.setLanguage('en_US')


current = lcu.get('/lol-perks/v1/currentpage').json()['id']
data = {'autoModifiedSelections': [],
        'current': False,
        'id': 908851014,
        'isActive': False,
        'isDeletable': True,
        'isEditable': True,
        'isValid': True,
        'lastModified': 1647086611516,
        'name': 'Tfuj stary',
        'order': 2,
        'primaryStyleId': 8100,
        'selectedPerkIds': [9923, 8143, 8138, 8134, 8233, 8236, 5005, 5008, 5001],
        'subStyleId': 8200
    }

print(lcu.get('/lol-perks/v1/perks').json())
#print(lcu.put(f'/lol-perks/v1/pages/{current}', data=json.dumps(data)))
