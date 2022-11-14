from fastapi import FastAPI, HTTPException, status
from main import LCU
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=['*'],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Set-Cookie"],
)


@app.get("/")
async def root():
    global lcu
    
    images = []


    try:
        lcu = LCU()
    except:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not running")
    
    
    try:
        picks = lcu.getPlayersPicks()
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="You're not in game")

    for i in picks[0]:


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

        if i not in lcu.getAllChampions():
            print(f"There's no champion named: {i}")

        lcu.champion = i
        images.append(lcu.getChampionImage())
        
    if picks[1]:
        lcu.champion = picks[1]['alias']
    else:
        return {"picks": picks[0], "images": images, "mypick": status.HTTP_404_NOT_FOUND}
    
    myChampImage = lcu.getChampionImage()
    
    
    return {"picks": picks[0], "images": images, "mypick": {"data": picks[1], "image": myChampImage}}


@app.get("/runes")
def runes():


    try:
        picks = lcu.getPlayersPicks()[1]
    except:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You're not in game. You can select champion to set runes in input below")


    if picks:
        lcu.champion = picks['alias']
        lcu.importRunes()
        return status.HTTP_201_CREATED
    else:
        return {"message": "Select champion first"}
