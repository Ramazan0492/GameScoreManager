# schemas.py
from pydantic import BaseModel

# Wat we van de gebruiker verwachten als ze een account maken:
class SpelerCreate(BaseModel):
    username: str
    password: str  # Hier typt de speler zijn wachtwoord in (bijv. "geheim123")

# Wat we terugsturen als we speler-data laten zien (GEEN wachtwoord!):
class SpelerResponse(BaseModel):
    id: int
    username: str

    class Config:
         from_attributes = True
        # In nieuwere versies van Pydantic / FastAPI mag je hier ook gebruiken:
        # from_attributes = True 

class NieuweScore(BaseModel):
    score: int