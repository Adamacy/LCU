from base64 import b64encode
import requests, json, asyncio
from exceptions import Errors

exceptions = Errors()

class Api:
    """
    Main class \n
    Using for connecting to League of Legends launcher. \n
    You can take data about all champions in the game, champions in champion select etc.
    """
    lang = None
    
    def __init__(self) -> None:
        try:
            file = open('D:/Riot Games/League of Legends/lockfile', 'r')
            self.data = file.read().split(':')
        except FileNotFoundError:
            raise exceptions.gameNotStarted()

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
        """Method get for websocket"""
        self.conn = requests.get(f'{self.uri}:{self.port}{endpoint}', verify=self.certificate, headers=self.headers, data = data)
        return self.conn
        

    def post(self, endpoint: str, data = {}):
        """Method post for websocket"""
        self.conn = requests.post(f'{self.uri}:{self.port}{endpoint}', verify=self.certificate, headers=self.headers, data = data)
        return self.conn


    def put(self, endpoint: str, data = {}): 
        """Method put for websocket"""       
        self.conn = requests.put(f'{self.uri}:{self.port}{endpoint}', verify=self.certificate, headers=self.headers, data = data)
        return self.conn


    def delete(self, endpoint: str, data = {}):
        """Method delete for websocket"""
        self.conn = requests.delete(f'{self.uri}:{self.port}{endpoint}', verify=self.certificate, headers=self.headers, data = data)
        return self.conn


    def patch(self, endpoint: str, data = {}):
        """Method patch for websocket"""
        self.conn = requests.patch(f'{self.uri}:{self.port}{endpoint}', verify=self.certificate, headers=self.headers, data = data)
        return self.conn

    def langauges(self):
        """List of API avaiable languages """
        lang = requests.get('https://ddragon.leagueoflegends.com/cdn/languages.json').json()
        return lang

    def setLanguage(self, lang: str):
        """Sets language. Using for API response."""
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
        """Returns all champions avaiable in game"""
        champions = requests.get('http://ddragon.leagueoflegends.com/cdn/12.5.1/data/en_US/champion.json')
        return list(champions.json()['data'].keys())


    def getChampData(self, champion: str):
        """Returns all informations about champion"""
        champion = champion.capitalize()
        if self.lang == None:
            raise exceptions.languageNotSet()
        if champion not in self.getAllChampions():
            raise exceptions.championWrongName()
        info = requests.get(f'http://ddragon.leagueoflegends.com/cdn/12.5.1/data/{self.lang}/champion/{champion}.json')
       
        return info.json()


