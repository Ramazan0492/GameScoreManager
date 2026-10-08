# auth.py
import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

SECRET_KEY = "mijn_super_geheime_ter_aa_sleutel"
ALGORITHM = "HS256"

# Dit zorgt voor het groene hangslotje in Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 1. Functie om wachtwoord te versleutelen
def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')

# 2. Functie om ingevuld wachtwoord te checken
def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode('utf-8')
    hash_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hash_bytes)

# 3. Functie om het inlog-token (polsbandje) te maken
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 4. De "Uitsmijter" die checkt of je bent ingelogd
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Niet geautoriseerd")
        return username
    except:
        raise HTTPException(status_code=401, detail="Ongeldig token")