from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Dit is de naam en locatie van je database-bestand (wordt straks vanzelf aangemaakt)
SQLALCHEMY_DATABASE_URL = "sqlite:///./game.db"

# 2. De 'engine' is de motor die de verbinding met SQLite regelt
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Een 'Session' is een tijdelijk gesprekskanaal om data te lezen of schrijven
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 'Base' is de blauwdruk. Hierop baseren we straks onze tabellen
Base = declarative_base()