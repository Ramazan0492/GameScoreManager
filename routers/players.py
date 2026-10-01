# routers/players.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal

# Maak de router aan (dit is eigenlijk een mini-FastAPI appje voor spelers)
router = APIRouter(
    prefix="/players", # Zet automatisch /players voor elke route in dit bestand
    tags=["Spelers"]
)

# Hulpfunctie voor de database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET: Alle spelers ophalen (Omdat we prefix="/players" gebruiken, is de URL hier gewoon "/")
@router.get("/")
def get_players(db: Session = Depends(get_db)):
    spelers = db.query(models.Player).all()
    return spelers

# POST: Nieuwe speler toevoegen
@router.post("/", status_code=201)
def voeg_speler_toe(speler: schemas.NieuweSpeler, db: Session = Depends(get_db)):
    nieuwe_speler = models.Player(username=speler.username)
    db.add(nieuwe_speler)
    db.commit()
    db.refresh(nieuwe_speler)
    return nieuwe_speler

# GET: Eén specifieke speler zoeken
@router.get("/{speler_id}")
def get_speler(speler_id: int, db: Session = Depends(get_db)):
    speler = db.query(models.Player).filter(models.Player.id == speler_id).first()
    if not speler:
        raise HTTPException(status_code=404, detail="Speler niet gevonden")
    return speler

# PUT: Bestaande speler wijzigen
@router.put("/{speler_id}")
def update_speler(speler_id: int, update_data: schemas.NieuweSpeler, db: Session = Depends(get_db)):
    speler = db.query(models.Player).filter(models.Player.id == speler_id).first()
    if not speler:
        raise HTTPException(status_code=404, detail="Speler niet gevonden om te wijzigen")
    speler.username = update_data.username
    db.commit()
    db.refresh(speler)
    return {"bericht": f"Speler {speler_id} succesvol gewijzigd", "nieuwe_data": speler}

# DELETE: Speler verwijderen
@router.delete("/{speler_id}")
def verwijder_speler(speler_id: int, db: Session = Depends(get_db)):
    speler = db.query(models.Player).filter(models.Player.id == speler_id).first()
    if not speler:
        raise HTTPException(status_code=404, detail="Speler niet gevonden om te verwijderen")
    db.delete(speler)
    db.commit()
    return {"bericht": f"Speler {speler_id} is succesvol verwijderd!"}