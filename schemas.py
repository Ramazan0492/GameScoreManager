from pydantic import BaseModel

class NieuweSpeler(BaseModel):
    username: str

class NieuweScore(BaseModel):
    score: int