from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import schemas
import crud
from database import SessionLocal

router = APIRouter(tags=["Scores"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/players/{speler_id}/scores", status_code=201)
def voeg_score_toe(speler_id: int, score_data: schemas.NieuweScore, db: Session = Depends(get_db)):
    speler = crud.get_speler(db, speler_id=speler_id)
    if not speler:
        raise HTTPException(status_code=404, detail="Speler niet gevonden")
    return crud.create_score(db=db, speler_id=speler_id, score_data=score_data)

@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    return crud.get_leaderboard(db)