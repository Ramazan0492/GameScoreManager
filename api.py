from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Importeer je database configuratie en modellen
import models
from database import engine, SessionLocal

# Maak de tabellen aan in de SQLite database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Hulpfunctie om voor elk request de database te openen en weer te sluiten
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# PYDANTIC MODELLEN (Uitsmijters voor de API)
class NieuweSpeler(BaseModel):
    username: str
    # 'id' en 'score' zijn hier weggehaald, want de database regelt ID's en scores staan in een eigen tabel

class NieuweScore(BaseModel):
    score: int


# ENDPOINTS

@app.get("/")
def test_api():
    return {"bericht": "Mijn database-gekoppelde FastAPI server draait!"}

# GET: Alle spelers ophalen uit de database
@app.get("/players")
def get_players(db: Session = Depends(get_db)):
    spelers = db.query(models.Player).all()
    return spelers

# POST: Nieuwe speler toevoegen (CREATE)
@app.post("/players", status_code=201)
def voeg_speler_toe(speler: NieuweSpeler, db: Session = Depends(get_db)):
    # Maak een nieuw Player object aan op basis van ons model
    nieuwe_speler = models.Player(username=speler.username)
    
    # Voeg toe aan de database en sla op
    db.add(nieuwe_speler)
    db.commit()
    db.refresh(nieuwe_speler)
    
    return nieuwe_speler

# GET: Eén specifieke speler zoeken
@app.get("/players/{speler_id}")
def get_speler(speler_id: int, db: Session = Depends(get_db)):
    speler = db.query(models.Player).filter(models.Player.id == speler_id).first()
    
    if not speler:
        raise HTTPException(status_code=404, detail="Speler niet gevonden")
        
    return speler

# POST: Een score toevoegen aan een specifieke speler
@app.post("/players/{speler_id}/scores", status_code=201)
def voeg_score_toe(speler_id: int, score_data: NieuweScore, db: Session = Depends(get_db)):
    # Controleer eerst of de speler wel bestaat
    speler = db.query(models.Player).filter(models.Player.id == speler_id).first()
    if not speler:
        raise HTTPException(status_code=404, detail="Speler niet gevonden")
        
    # Koppel de nieuwe score aan het ID van de speler (Foreign Key)
    nieuwe_score = models.Score(score=score_data.score, player_id=speler_id)
    db.add(nieuwe_score)
    db.commit()
    db.refresh(nieuwe_score)
    
    return nieuwe_score

# GET: Leaderboard ophalen
@app.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    # Haal alle scores op en sorteer ze van hoog naar laag
    scores = db.query(models.Score).order_by(models.Score.score.desc()).all()
    return scores

# PUT: Bestaande speler wijzigen (UPDATE)
@app.put("/players/{speler_id}")
def update_speler(speler_id: int, update_data: NieuweSpeler, db: Session = Depends(get_db)):
    speler = db.query(models.Player).filter(models.Player.id == speler_id).first()
    
    if not speler:
        raise HTTPException(status_code=404, detail="Speler niet gevonden om te wijzigen")
        
    # Update de naam en sla op
    speler.username = update_data.username
    db.commit()
    db.refresh(speler)
    
    return {"bericht": f"Speler {speler_id} succesvol gewijzigd", "nieuwe_data": speler}

# DELETE: Speler verwijderen (DELETE)
@app.delete("/players/{speler_id}")
def verwijder_speler(speler_id: int, db: Session = Depends(get_db)):
    speler = db.query(models.Player).filter(models.Player.id == speler_id).first()
    
    if not speler:
        raise HTTPException(status_code=404, detail="Speler niet gevonden om te verwijderen")
        
    # Verwijder de speler uit de database
    db.delete(speler)
    db.commit()
    
    return {"bericht": f"Speler {speler_id} is succesvol verwijderd!"}