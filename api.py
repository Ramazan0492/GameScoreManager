import json
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def test_api():
    return {"bericht": "Mijn eerste FastAPI server draait!"}

@app.get("/players")
def get_players():
    try:
        with open("spelers.json", "r") as file:
            spelers = json.load(file)
            return spelers
    except FileNotFoundError:
        return []

# Nieuw endpoint om één specifieke speler op te zoeken
@app.get("/players/{speler_id}")
def get_speler(speler_id: str):
    try:
        with open("spelers.json", "r") as file:
            spelers = json.load(file)
            
            # Loop door de spelers om te kijken of het ID overeenkomt
            for speler in spelers:
                if speler["id"] == speler_id:
                    return speler  # Speler gevonden! Stuur deze ene speler terug.
            
            # Als de loop klaar is en niks heeft gevonden, gooien we een 404 error
            raise HTTPException(status_code=404, detail="Speler niet gevonden")
            
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Geen spelersbestand gevonden")

# Nieuw endpoint voor het leaderboard
@app.get("/leaderboard")
def get_leaderboard():
    try:
        with open("spelers.json", "r") as file:
            spelers = json.load(file)
            
            # We sorteren de lijst op basis van de "score" in de JSON-data
            # reverse=True zorgt ervoor dat de hoogste score bovenaan staat
            gesorteerde_spelers = sorted(spelers, key=lambda speler: speler["score"], reverse=True)
            
            return gesorteerde_spelers
            
    except FileNotFoundError:
        return []