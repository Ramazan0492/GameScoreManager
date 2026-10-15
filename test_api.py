from fastapi.testclient import TestClient
from main import app

# Virtuele test-client voor het simuleren van API-verzoeken
client = TestClient(app)

# Test of de API succesvol een lijst met spelers kan ophalen (Happy flow).
def test_haal_spelers_op():
    response = client.get("/players/")
    assert response.status_code == 200

# Test of het opvragen van een onbekend ID netjes een 404-foutmelding geeft in plaats van een crash.
def test_haal_niet_bestaande_speler_op():
    response = client.get("/players/9999")
    assert response.status_code == 404 

# Test de beveiliging: controleert of acties zonder inlog-token direct worden geweigerd (401).
def test_verwijder_speler_zonder_login_wordt_geblokkeerd():
    response = client.delete("/players/1")
    assert response.status_code == 401       

# Test of FastAPI/Pydantic foute invoer (letters i.p.v. cijfers in de URL) afvangt met een 422-validatiefout.
def test_ongeldige_invoer_geeft_nette_foutmelding():
    response = client.get("/players/abc")
    assert response.status_code == 422

# Test of de database-error handling werkt: voorkomt een 500-crash bij het aanmaken van een bestaande gebruikersnaam.
def test_dubbele_speler_geeft_nette_error():
    client.post("/players/", json={"username": "TestKees", "password": "123"})
    response = client.post("/players/", json={"username": "TestKees", "password": "123"})
    assert response.status_code != 500