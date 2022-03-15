from base64 import b64encode
import requests, json

class Api:

    def __init__(self) -> None:



        file = open('/home/adam/Games/league-of-legends/drive_c/Riot Games/League of Legends/lockfile', 'r')
        self.data = file.read().split(':')
        self.certificate = 'cer.pem'
        self.uri = 'https://127.0.0.1'
        self.port = self.data[2]
        self.password = self.data[3]
        self.endpoint = None
        self.data = None



    def connect(self, method: str, endpoint: str, data = {}):
        '''Connect to websocket '''
        auth = f'riot:{self.password}'.encode('ascii')

        headers = {
            'Authorization': f"Basic {b64encode(auth).decode('ascii')}",
            'Content-type': 'application/json'
        }

        if method == 'get':
            self.conn = requests.get(f'{self.uri}:{self.port}/{endpoint}', verify=self.certificate, headers=headers, data = data)
        
        elif method == 'post':
            self.conn = requests.post(f'{self.uri}:{self.port}/{endpoint}', verify=self.certificate, headers=headers, data = data)

        elif method == 'put':
            self.conn = requests.put(f'{self.uri}:{self.port}/{endpoint}', verify=self.certificate, headers=headers, data = data)

        elif method == 'delete':
            self.conn = requests.delete(f'{self.uri}:{self.port}/{endpoint}', verify=self.certificate, headers=headers, data = data)

        elif method == 'patch':
            self.conn = requests.patch(f'{self.uri}:{self.port}/{endpoint}', verify=self.certificate, headers=headers, data = data)
        

        return self.conn



summonerID = 82386223
accountID = 2285688008995680
puuid = '55ffad8e-83d4-5d8d-8c8e-05e3d13f556d'


lcu = Api()
print(lcu.connect('get', f'lol-item-sets/v1/item-sets/{summonerID}/sets').json())