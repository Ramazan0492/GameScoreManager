from fastapi.testclient import TestClient
from main import app

# We maken een virtuele test-gebruiker (client) aan
client = TestClient(app)

def test_haal_spelers_op():
    # De robot simuleert een klik op GET /players/
    response = client.get("/players/")

    # We eisen (assert) dat de server antwoordt met code 200 (OK)
    assert response.status_code == 200

def test_haal_niet_bestaande_speler_op():
    # De robot simuleert het ophalen van een ID dat niet bestaat
    response = client.get("/players/9999")
    
    # We eisen dat de API niet crasht, maar een nette 404 Not Found error geeft
    assert response.status_code == 404 

def test_verwijder_speler_zonder_login_wordt_geblokkeerd():
    # De robot probeert een speler te verwijderen, maar logt NIET in
    response = client.delete("/players/1")
    
    # We eisen dat de API dit weigert met een 401 Unauthorized code
    assert response.status_code == 401       

def test_ongeldige_invoer_geeft_nette_foutmelding():
    # De robot typt letters in de URL in plaats van een ID-nummer
    response = client.get("/players/abc")
    
    # We eisen dat Pydantic dit afvangt en code 422 (Validation Error) geeft
    assert response.status_code == 422

def test_dubbele_speler_geeft_nette_error():
    # 1. De robot maakt een nieuwe speler aan
    client.post("/players/", json={"username": "TestKees", "password": "123"})
    
    # 2. De robot probeert exact dezelfde speler NÓG een keer aan te maken
    response = client.post("/players/", json={"username": "TestKees", "password": "123"})
    
    # 3. We eisen dat de API dit netjes afvangt (bijv. code 400), en NIET crasht (code 500)
    assert response.status_code != 500