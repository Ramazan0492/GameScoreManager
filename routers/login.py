# routers/login.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import crud
import auth
from database import SessionLocal

router = APIRouter(tags=["Authenticatie"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Zoek de speler op basis van de ingevulde username
    speler = crud.get_speler_by_username(db, username=form_data.username)
    if not speler:
        raise HTTPException(status_code=400, detail="Inloggegevens onjuist")
    
    # 2. Controleer of het wachtwoord klopt
    if not auth.verify_password(form_data.password, speler.hashed_password):
        raise HTTPException(status_code=400, detail="Inloggegevens onjuist")
    
    # 3. Alles klopt! Maak het token aan
    access_token = auth.create_access_token(data={"sub": speler.username})
    
    # FastAPI eist exact deze opbouw voor de output:
    return {"access_token": access_token, "token_type": "bearer"}