from base64 import b64encode
import requests
import json
import asyncio
from exceptions import Errors
from bs4 import BeautifulSoup
import runes


exceptions = Errors()

class Api:

    lang = 'en_US'
    champion = None
    def __init__(self) -> None:

        file = open(
            'C:/Riot Games/League of Legends/lockfile', 'r')
        self.data = file.read().split(':')
        self.certificate = 'LCU/cer.pem'
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
        champion = champion.capitalize()
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
            for i in session['actions'][1]:
                if i[1]['type'] == 'ban':
                    continue
                else:
                    print(i)
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
        
        return list(champions.json()['data'].keys())

    def getChampStats(self):
        if self.lang == None:
            raise exceptions.languageNotSet()
        if self.champion not in list(self.getAllChampions()['data'].keys()):
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

        champion = champion.capitalize()

        data = self.getChampStats(self.champion)['data'][self.champion]
        i = data['image']['full']
        return f'http://ddragon.leagueoflegends.com/cdn/12.5.1/img/champion/{i}'

    def getChampionSpells(self):
        """Returns an array of champion spells and passive"""

        data = self.getChampStats(self.champion)['data'][self.champion]
        self.spellNames = []
        for spell in data['spells']:
            self.spellNames.append(spell['name'])
        self.spellNames.append(data['passive']['name'])

        return self.spellNames

    def getSpellsImage(self):
        """Return images of all champion spells"""
        data = self.getChampStats(self.champion)['data'][self.champion]
        images = []
        for i in data['spells']:
            i = i['image']['full']
            spellImage = f'http://ddragon.leagueoflegends.com/cdn/12.5.1/img/spell/{i}'
            images.append(spellImage)

        passive = f"http://ddragon.leagueoflegends.com/cdn/12.5.1/img/passive/{data['passive']['image']['full']}"
        images.append(passive)

        return images

    def getAllRunes(self):

        res = requests.get('')

    def getChampBuild(self):
        """Returns names of best build for selected champion"""
        return runes.getRunes(self.champion)

    def importRunes(self):

        id = self.get('/lol-perks/v1/currentpage').json()['id']

        
        data = {'autoModifiedSelections': [], 'current': True, 'id': id, 'isActive': False, 'isDeletable': True, 'isEditable': True, 'isValid': True, 'lastModified': 1647681656447, 'name': 'New Runes Page 2', 'order': 1, 'primaryStyleId': 8100, 'selectedPerkIds': [], 'subStyleId': 8000}


        cos = self.getChampBuild()
        for i in self.get('/lol-perks/v1/perks').json():
            if i['name'] in cos:
                print(i['name'] ,i['id'])
                data['selectedPerkIds'].append(i['id'])
        print(data['selectedPerkIds'])
        res = self.put(f'/lol-perks/v1/pages/{id}', data=json.dumps(data))
        print(self.post('/lol-perks/v1/pages', data=json.dumps(data)).json())
        return res
