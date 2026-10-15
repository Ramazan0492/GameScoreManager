from pydantic import BaseModel

# Wat we van de gebruiker verwachten als ze een account maken:
class SpelerCreate(BaseModel):
    username: str
    password: str  

# Wat we terugsturen als we speler-data laten zien:
class SpelerResponse(BaseModel):
    id: int
    username: str
    is_admin: bool  

    class Config:
        from_attributes = True

class NieuweScore(BaseModel):
    score: int