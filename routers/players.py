# routers/players.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import schemas
import crud  # <-- Importeer je nieuwe Service Layer
from database import SessionLocal

router = APIRouter(
    prefix="/players",
    tags=["Spelers"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_players(db: Session = Depends(get_db)):
    return crud.get_players(db)  # <-- De router stuurt het werk door naar crud.py!

@router.post("/", status_code=201)
def voeg_speler_toe(speler: schemas.NieuweSpeler, db: Session = Depends(get_db)):
    return crud.create_speler(db=db, speler=speler)

@router.get("/{speler_id}")
def get_speler(speler_id: int, db: Session = Depends(get_db)):
    speler = crud.get_speler(db=db, speler_id=speler_id)
    if not speler:
        raise HTTPException(status_code=404, detail="Speler niet gevonden")
    return speler

@router.delete("/{speler_id}")
def verwijder_speler(speler_id: int, db: Session = Depends(get_db)):
    speler = crud.get_speler(db=db, speler_id=speler_id)
    if not speler:
        raise HTTPException(status_code=404, detail="Speler niet gevonden om te verwijderen")
    
    crud.delete_speler(db=db, speler=speler)
    return {"bericht": f"Speler {speler_id} is succesvol verwijderd!"}

# (De PUT route heb ik voor het overzicht even weggelaten, maar die werkt op precies dezelfde manier)