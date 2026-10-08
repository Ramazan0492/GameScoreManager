# routers/players.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import schemas
import crud  # <-- Importeer je Service Layer
import auth  # <-- Nieuwe import voor de beveiliging!
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

# GET: Haal alle spelers op (Beveiligd: geeft een lijst zonder wachtwoorden terug)
@router.get("/", response_model=list[schemas.SpelerResponse])
def get_players(db: Session = Depends(get_db)):
    return crud.get_players(db)

# POST: Nieuwe speler toevoegen (Input: SpelerCreate met wachtwoord, Output: SpelerResponse ZONDER wachtwoord)
@router.post("/", status_code=201, response_model=schemas.SpelerResponse)
def voeg_speler_toe(speler: schemas.SpelerCreate, db: Session = Depends(get_db)):
    return crud.create_speler(db=db, speler=speler)

# GET: Eén specifieke speler zoeken (Beveiligd: zonder wachtwoord)
@router.get("/{speler_id}", response_model=schemas.SpelerResponse)
def get_speler(speler_id: int, db: Session = Depends(get_db)):
    speler = crud.get_speler(db=db, speler_id=speler_id)
    if not speler:
        raise HTTPException(status_code=404, detail="Speler niet gevonden")
    return speler

# DELETE: Speler verwijderen (Nu beveiligd met Autorisatie!)
@router.delete("/{speler_id}")
def verwijder_speler(
    speler_id: int, 
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)  
):
    speler = crud.get_speler(db=db, speler_id=speler_id)
    if not speler:
        raise HTTPException(status_code=404, detail="Speler niet gevonden")
    
    # De Autorisatie-check: Ben jij wel de eigenaar van dit account?
    if speler.username != current_user:
        raise HTTPException(status_code=403, detail="Je mag alleen je eigen account verwijderen!")
    
    crud.delete_speler(db=db, speler=speler)
    return {"bericht": f"Account van {speler.username} is succesvol verwijderd!"}