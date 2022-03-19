from main import Api
import random

lcu = Api()

cos = lcu.getAllChampions()
lcu.setChampion(random.choice(cos))

print(lcu.importRunes().json())