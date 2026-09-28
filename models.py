from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Tabel 1: De speler
class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)

    # Dit vertelt SQLAlchemy dat deze speler meerdere scores kan hebben
    scores = relationship("Score", back_populates="player")

# Tabel 2: De scores
class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)
    
    # De Foreign Key: Dit koppelt de score aan het unieke ID van een speler
    player_id = Column(Integer, ForeignKey("players.id"))

    # Dit vertelt SQLAlchemy dat deze score bij één specifieke speler hoort
    player = relationship("Player", back_populates="scores")