from database import SessionLocal
import models

# Open de verbinding met de database
db = SessionLocal()

# Zoek jouw account op
admin_speler = db.query(models.Player).filter(models.Player.username == "ram").first()

if admin_speler:
    admin_speler.is_admin = True
    db.commit()
    print(f"Succes! Speler '{admin_speler.username}' is nu een ADMIN.")
else:
    print("Speler niet gevonden.")

db.close()