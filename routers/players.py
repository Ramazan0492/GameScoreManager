# routers/players.py
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
import schemas
import crud  # <-- Importeer je Service Layer
import auth  # <-- Beveiliging
import models # <-- Toegevoegd om de admin-status uit de database te halen
from database import SessionLocal
from sqlalchemy.exc import IntegrityError

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

# POST: Nieuwe speler toevoegen 
@router.post("/", status_code=201, response_model=schemas.SpelerResponse)
def voeg_speler_toe(speler: schemas.SpelerCreate, db: Session = Depends(get_db)):
    try:
        # Probeer de speler aan te maken
        return crud.create_speler(db=db, speler=speler)
    except IntegrityError:
        # Raakt de database in paniek (bijv. door een dubbele naam)? 
        # Voorkom de 500 crash, herstel de database en geef een nette 400 error.
        db.rollback() 
        raise HTTPException(status_code=400, detail="Deze gebruikersnaam is al in gebruik!")

# GET: Eén specifieke speler zoeken (Beveiligd: zonder wachtwoord)
@router.get("/{speler_id}", response_model=schemas.SpelerResponse)
def get_speler(speler_id: int, db: Session = Depends(get_db)):
    speler = crud.get_speler(db=db, speler_id=speler_id)
    if not speler:
        raise HTTPException(status_code=404, detail="Speler niet gevonden")
    return speler

# DELETE: Speler verwijderen (Nu beveiligd: Alleen een ADMIN mag dit!)
@router.delete("/{speler_id}")
def verwijder_speler(
    speler_id: int, 
    db: Session = Depends(get_db),
    current_user_name: str = Depends(auth.get_current_user)  
):
    # 1. Zoek de ingelogde gebruiker op in de database om zijn admin-status te checken
    ingelogde_gebruiker = db.query(models.Player).filter(models.Player.username == current_user_name).first()
    
    # 2. De Autorisatie-check: Is de ingelogde gebruiker wel een admin?
    if not ingelogde_gebruiker or not ingelogde_gebruiker.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Je hebt geen admin rechten om accounts te verwijderen!"
        )

    # 3. Zoek de speler die we willen verwijderen
    speler = crud.get_speler(db=db, speler_id=speler_id)
    if not speler:
        raise HTTPException(status_code=404, detail="Speler niet gevonden")
    
    # 4. Verwijder de speler
    crud.delete_speler(db=db, speler=speler)
    return {"bericht": f"Account van {speler.username} is succesvol verwijderd!"}