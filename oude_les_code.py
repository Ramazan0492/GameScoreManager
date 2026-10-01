import json
from player import Player

spelers_lijst = []
BESTAND = "spelers.json"

def laad_gegevens():
    # Probeert het bestand te openen. Als het niet bestaat (eerste keer), negeert hij de fout.
    try:
        with open(BESTAND, "r") as file:
            opgeslagen_data = json.load(file)
            for data in opgeslagen_data:
                # Maak de Player objecten weer aan met de opgeslagen data
                spelers_lijst.append(Player(data["id"], data["username"], data["score"]))
    except FileNotFoundError:
        pass

def sla_gegevens_op():
    # Maak een simpele lijst van de gegevens om op te slaan in JSON
    data_om_te_bewaren = []
    for speler in spelers_lijst:
        data_om_te_bewaren.append({"id": speler.id, "username": speler.username, "score": speler.score})
    
    with open(BESTAND, "w") as file:
        json.dump(data_om_te_bewaren, file, indent=4)
    print("Gegevens succesvol opgeslagen in spelers.json!")

def haal_score_op(speler):
    return speler.score

def toon_menu():
    print("\n--- Game Score Manager ---")
    print("1. Speler toevoegen")
    print("2. Alle spelers bekijken")
    print("3. Speler zoeken")
    print("4. Score wijzigen")
    print("5. Leaderboard bekijken")
    print("6. Afsluiten")

def voeg_speler_toe():
    print("\nNieuwe speler toevoegen:")
    speler_id = input("Wat is het ID van de speler? ")
    naam = input("Wat is de gebruikersnaam? ")
    
    while True:
        try:
            score = int(input("Wat is de score? (Vul een getal in): "))
            break
        except ValueError:
            print("Fout: Dat is geen geldig getal! Probeer het opnieuw.")
    
    nieuwe_speler = Player(speler_id, naam, score)
    spelers_lijst.append(nieuwe_speler)
    print(f"Succes! Speler {naam} is toegevoegd.")

def bekijk_spelers():
    print("\nLijst met spelers:")
    if len(spelers_lijst) == 0:
        print("Er zijn nog geen spelers toegevoegd.")
    else:
        for speler in spelers_lijst:
            print(f"ID: {speler.id} | Naam: {speler.username} | Score: {speler.score}")

def zoek_speler():
    print("\nSpeler zoeken:")
    zoek_naam = input("Welke gebruikersnaam zoek je? ")
    gevonden = False
    
    for speler in spelers_lijst:
        if speler.username.lower() == zoek_naam.lower():
            print(f"Speler gevonden! ID: {speler.id} | Naam: {speler.username} | Score: {speler.score}")
            gevonden = True
            break 
            
    if gevonden == False:
        print("Helaas, die speler staat niet in de lijst.")

def wijzig_score():
    print("\nScore wijzigen:")
    zoek_naam = input("Van welke speler wil je de score wijzigen? ")
    gevonden = False
    
    for speler in spelers_lijst:
        if speler.username.lower() == zoek_naam.lower():
            print(f"Huidige score van {speler.username} is: {speler.score}")
            while True:
                try:
                    nieuwe_score = int(input("Wat is de nieuwe score? "))
                    speler.score = nieuwe_score
                    break
                except ValueError:
                    print("Fout: Dat is geen geldig getal!")
            
            print(f"Succes! De score van {speler.username} is nu {speler.score}.")
            gevonden = True
            break
            
    if gevonden == False:
        print("Helaas, die speler staat niet in de lijst.")

def toon_leaderboard():
    print("\n--- LEADERBOARD ---")
    if len(spelers_lijst) == 0:
        print("Er zijn nog geen spelers om te sorteren.")
    else:
        spelers_lijst.sort(key=haal_score_op, reverse=True)
        positie = 1
        for speler in spelers_lijst:
            print(f"{positie}. {speler.username} - Score: {speler.score}")
            positie += 1

# --- HOOFDPROGRAMMA ---

# Direct bij het opstarten laden we de oude gegevens in
laad_gegevens()

while True:
    toon_menu()
    keuze = input("Kies een optie (1-6): ")

    if keuze == "1":
        voeg_speler_toe()
    elif keuze == "2":
        bekijk_spelers()
    elif keuze == "3":
        zoek_speler()
    elif keuze == "4":
        wijzig_score()
    elif keuze == "5":
        toon_leaderboard()
    elif keuze == "6":
        # Voordat we afsluiten, slaan we de actuele lijst op
        sla_gegevens_op()
        print("Programma sluit af. Tot ziens!")
        break
    else:
        print("Ongeldige invoer. Kies 1, 2, 3, 4, 5 of 6.")