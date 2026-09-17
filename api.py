import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# 1. HET PYDANTIC MODEL (De uitsmijter voor nieuwe/gewijzigde data)
class NieuweSpeler(BaseModel):
    id: str
    username: str
    score: int

# 2. ALLE ENDPOINTS

@app.get("/")
def test_api():
    return {"bericht": "Mijn eerste FastAPI server draait!"}

# GET: Alle spelers ophalen
@app.get("/players")
def get_players():
    try:
        with open("spelers.json", "r") as file:
            spelers = json.load(file)
            return spelers
    except FileNotFoundError:
        return []

# POST: Nieuwe speler toevoegen (CREATE)
@app.post("/players", status_code=201)
def voeg_speler_toe(speler: NieuweSpeler):
    try:
        with open("spelers.json", "r") as file:
            spelers = json.load(file)
    except FileNotFoundError:
        spelers = []
        
    spelers.append(speler.model_dump())
    
    with open("spelers.json", "w") as file:
        json.dump(spelers, file, indent=4)
        
    return speler

# GET: Eén specifieke speler zoeken
@app.get("/players/{speler_id}")
def get_speler(speler_id: str):
    try:
        with open("spelers.json", "r") as file:
            spelers = json.load(file)
            
            for speler in spelers:
                if speler["id"] == speler_id:
                    return speler  
            
            raise HTTPException(status_code=404, detail="Speler niet gevonden")
            
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Geen spelersbestand gevonden")

# GET: Leaderboard
@app.get("/leaderboard")
def get_leaderboard():
    try:
        with open("spelers.json", "r") as file:
            spelers = json.load(file)
            
            gesorteerde_spelers = sorted(spelers, key=lambda speler: speler["score"], reverse=True)
            return gesorteerde_spelers
            
    except FileNotFoundError:
        return []

# PUT: Bestaande speler wijzigen (UPDATE)
@app.put("/players/{speler_id}")
def update_speler(speler_id: str, update_data: NieuweSpeler):
    try:
        with open("spelers.json", "r") as file:
            spelers = json.load(file)
            
        for speler in spelers:
            if speler["id"] == speler_id:
                speler["username"] = update_data.username
                speler["score"] = update_data.score
                
                with open("spelers.json", "w") as file:
                    json.dump(spelers, file, indent=4)
                    
                return {"bericht": f"Speler {speler_id} succesvol gewijzigd", "nieuwe_data": speler}
                
        raise HTTPException(status_code=404, detail="Speler niet gevonden om te wijzigen")
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Geen database gevonden")

# DELETE: Speler verwijderen (DELETE)
@app.delete("/players/{speler_id}")
def verwijder_speler(speler_id: str):
    try:
        with open("spelers.json", "r") as file:
            spelers = json.load(file)
            
        nieuwe_lijst = [speler for speler in spelers if speler["id"] != speler_id]
        
        if len(spelers) == len(nieuwe_lijst):
            raise HTTPException(status_code=404, detail="Speler niet gevonden om te verwijderen")
            
        with open("spelers.json", "w") as file:
            json.dump(nieuwe_lijst, file, indent=4)
            
        return {"bericht": f"Speler {speler_id} is succesvol verwijderd!"}
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Geen database gevonden")