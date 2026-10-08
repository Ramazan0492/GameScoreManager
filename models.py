# models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)  # <-- Deze regel is nieuw!

    scores = relationship("Score", back_populates="player")

class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)
    player_id = Column(Integer, ForeignKey("players.id"))

    player = relationship("Player", back_populates="scores")