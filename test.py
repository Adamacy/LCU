from main import Api

lcu = Api()

cos = lcu.getAllChampions()
lcu.setChampion('Riven')

print(lcu.getChampBuild())