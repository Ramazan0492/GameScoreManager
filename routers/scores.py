# routers/scores.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal

# Maak de router aan voor scores
router = APIRouter(
    tags=["Scores"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST: Een score toevoegen aan een specifieke speler
@router.post("/players/{speler_id}/scores", status_code=201)
def voeg_score_toe(speler_id: int, score_data: schemas.NieuweScore, db: Session = Depends(get_db)):
    speler = db.query(models.Player).filter(models.Player.id == speler_id).first()
    if not speler:
        raise HTTPException(status_code=404, detail="Speler niet gevonden")
        
    nieuwe_score = models.Score(score=score_data.score, player_id=speler_id)
    db.add(nieuwe_score)
    db.commit()
    db.refresh(nieuwe_score)
    
    return nieuwe_score

# GET: Leaderboard ophalen
@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    scores = db.query(models.Score).order_by(models.Score.score.desc()).all()
    return scores