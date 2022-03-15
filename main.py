from base64 import b64encode
import requests

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



    def connect(self, method: str, endpoint: str):
        '''Connect to websocket '''
        auth = f'riot:{self.password}'.encode('ascii')

        headers = {
            'Authorization': f"Basic {b64encode(auth).decode('ascii')}"
        }
        if method == 'get':
            self.conn = requests.get(f'{self.uri}:{self.port}/{endpoint}', verify=self.certificate, headers=headers)
        
        elif method == 'post':
            self.conn = requests.post(f'{self.uri}:{self.port}/{endpoint}', verify=self.certificate, headers=headers)

        elif method == 'put':
            self.conn = requests.put(f'{self.uri}:{self.port}/{endpoint}', verify=self.certificate, headers=headers)

        elif method == 'delete':
            self.conn = requests.delete(f'{self.uri}:{self.port}/{endpoint}', verify=self.certificate, headers=headers)

        elif method == 'patch':
            self.conn = requests.patch
        
        
        return self.conn



lcu = Api()
print(lcu.connect('get', 'lol-summoner/v1/current-summoner').json())

'''
#Vars
f = open('/home/adam/Games/league-of-legends/drive_c/Riot Games/League of Legends/lockfile', 'r') #Path to lockfile
data = f.read().split(':')
password = data[3]
encodeAuth = f'riot:{password}'.encode('ascii')
base64Auth = b64encode(encodeAuth)

#Authorization for websocker
headers = {
    'Authorization': f"Basic {base64Auth.decode('ascii')}"
}


res = requests.get(f'https://127.0.0.1:{data[2]}/lol-summoner/v1/current-summoner', verify='cos/cer.pem', headers=headers)

print(res.json())
'''