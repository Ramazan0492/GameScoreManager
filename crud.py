# crud.py
from sqlalchemy.orm import Session
import models
import schemas

# READ: Alle spelers ophalen
def get_players(db: Session):
    return db.query(models.Player).all()

# READ: Eén speler ophalen
def get_speler(db: Session, speler_id: int):
    return db.query(models.Player).filter(models.Player.id == speler_id).first()

# CREATE: Nieuwe speler toevoegen
def create_speler(db: Session, speler: schemas.NieuweSpeler):
    nieuwe_speler = models.Player(username=speler.username)
    db.add(nieuwe_speler)
    db.commit()
    db.refresh(nieuwe_speler)
    return nieuwe_speler

# DELETE: Speler verwijderen
def delete_speler(db: Session, speler: models.Player):
    db.delete(speler)
    db.commit()

# CREATE: Nieuwe score toevoegen voor een speler
def create_score(db: Session, speler_id: int, score_data: schemas.NieuweScore):
    nieuwe_score = models.Score(score=score_data.score, player_id=speler_id)
    db.add(nieuwe_score)
    db.commit()
    db.refresh(nieuwe_score)
    return nieuwe_score

# READ: Leaderboard ophalen (gesorteerd van hoog naar laag)
def get_leaderboard(db: Session):
    return db.query(models.Score).order_by(models.Score.score.desc()).all()