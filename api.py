# api.py
from fastapi import FastAPI
import models
from database import engine
from routers import players, scores

# Maak de tabellen aan in de SQLite database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Koppel de routers aan de hoofdapplicatie
app.include_router(players.router)
app.include_router(scores.router)

# De test-route (dit is de allerlaatste route die hier nog in mag staan!)
@app.get("/")
def test_api():
    return {"bericht": "Mijn database-gekoppelde FastAPI server draait, en de code is perfect gestructureerd!"}