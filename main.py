from base64 import b64encode
import requests, json, asyncio
from exceptions import Errors

exceptions = Errors()

class Api:

    lang = None
    
    def __init__(self) -> None:

        file = open('/home/adam/Games/league-of-legends/drive_c/Riot Games/League of Legends/lockfile', 'r')
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
        self.conn = requests.get(f'{self.uri}:{self.port}{endpoint}', verify=self.certificate, headers=self.headers, data = data)
        return self.conn
        

    def post(self, endpoint: str, data = {}):
        self.conn = requests.post(f'{self.uri}:{self.port}{endpoint}', verify=self.certificate, headers=self.headers, data = data)
        return self.conn


    def put(self, endpoint: str, data = {}):        
        self.conn = requests.put(f'{self.uri}:{self.port}{endpoint}', verify=self.certificate, headers=self.headers, data = data)
        return self.conn


    def delete(self, endpoint: str, data = {}):
        self.conn = requests.delete(f'{self.uri}:{self.port}{endpoint}', verify=self.certificate, headers=self.headers, data = data)
        return self.conn


    def patch(self, endpoint: str, data = {}):
        self.conn = requests.patch(f'{self.uri}:{self.port}{endpoint}', verify=self.certificate, headers=self.headers, data = data)
        return self.conn

    def langauges(self):
        lang = requests.get('https://ddragon.leagueoflegends.com/cdn/languages.json').json()
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
                    champ = self.get(f'/lol-champions/v1/inventories/{self.summonerID}/champions/{championID}')
                    print(champ.json()['name'])
                    champions.append(champ.json()['name'])
            return champions
        except:
            raise exceptions.matchNotFound()


    def getAllChampions(self):
        champions = requests.get('http://ddragon.leagueoflegends.com/cdn/12.5.1/data/en_US/champion.json')
        return champions.json()


    def getChampStats(self, champion: str):
        if self.lang == None:
            raise exceptions.languageNotSet()
        if champion not in list(self.getAllChampions()['data'].keys()):
            raise exceptions.championWrongName()
        info = requests.get(f'http://ddragon.leagueoflegends.com/cdn/12.5.1/data/{self.lang}/champion/{champion}.json')
        
        return info.json()

    
lcu = Api()
lcu.setLanguage('pl_PL')
print(lcu.getPlayersPicks())