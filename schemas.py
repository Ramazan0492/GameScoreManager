from pydantic import BaseModel

# Wat we van de gebruiker verwachten als ze een account maken:
class SpelerCreate(BaseModel):
    username: str
    password: str  # Hier typt de speler zijn wachtwoord in (bijv. "geheim123")

# Wat we terugsturen als we speler-data laten zien:
class SpelerResponse(BaseModel):
    id: int
    username: str
    is_admin: bool  # <-- Nu staat hij in de juiste class!

    class Config:
        from_attributes = True

class NieuweScore(BaseModel):
    score: int