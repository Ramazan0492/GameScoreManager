from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
import schemas
import crud
import auth
import models
from database import SessionLocal
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/players",
    tags=["Spelers"]
)

# Maakt een database-sessie aan voor een inkomend verzoek en sluit deze netjes af
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Haalt een lijst op van alle spelers (geeft veilige data terug, zonder wachtwoorden)
@router.get("/", response_model=list[schemas.SpelerResponse])
def get_players(db: Session = Depends(get_db)):
    return crud.get_players(db)

# Maakt een nieuwe speler aan en geeft een 400-fout als de gebruikersnaam al bestaat
@router.post("/", status_code=201, response_model=schemas.SpelerResponse)
def voeg_speler_toe(speler: schemas.SpelerCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_speler(db=db, speler=speler)
    except IntegrityError:
        db.rollback() 
        raise HTTPException(status_code=400, detail="Deze gebruikersnaam is al in gebruik!")

# Zoekt één specifieke speler op basis van het ID
@router.get("/{speler_id}", response_model=schemas.SpelerResponse)
def get_speler(speler_id: int, db: Session = Depends(get_db)):
    speler = crud.get_speler(db=db, speler_id=speler_id)
    if not speler:
        raise HTTPException(status_code=404, detail="Speler niet gevonden")
    return speler

# Verwijdert een speler, maar controleert eerst of de ingelogde gebruiker admin-rechten heeft
@router.delete("/{speler_id}")
def verwijder_speler(
    speler_id: int, 
    db: Session = Depends(get_db),
    current_user_name: str = Depends(auth.get_current_user)  
):
    ingelogde_gebruiker = db.query(models.Player).filter(models.Player.username == current_user_name).first()
    
    if not ingelogde_gebruiker or not ingelogde_gebruiker.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Je hebt geen admin rechten om accounts te verwijderen!"
        )

    speler = crud.get_speler(db=db, speler_id=speler_id)
    if not speler:
        raise HTTPException(status_code=404, detail="Speler niet gevonden")
    
    crud.delete_speler(db=db, speler=speler)
    return {"bericht": f"Account van {speler.username} is succesvol verwijderd!"}