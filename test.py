from main import Api

lcu = Api()

lcu.setChampion('Shaco')

for i in lcu.getPlayersPicks():
    lcu.champion = i
    print(f'Counters for: {i}: {lcu.getCounters()}')
