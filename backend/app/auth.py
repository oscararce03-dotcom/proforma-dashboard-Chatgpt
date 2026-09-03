from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException, Header
from .config import JWT_SECRET, ADMIN_USERNAME, ADMIN_PASSWORD

ALGORITHM = "HS256"

# El usuario definido por Render corresponde a Gerencia General.
# Gerencia Comercial utiliza el mismo password configurado para la prueba inicial.
USERS = {
    ADMIN_USERNAME: {"password": ADMIN_PASSWORD, "role": "GERENCIA GENERAL"},
    "comercial": {"password": ADMIN_PASSWORD, "role": "GERENCIA COMERCIAL"},
}

def create_token(username: str, role: str):
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=8),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)

def authenticate(username: str, password: str):
    user = USERS.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    return create_token(username, user["role"])

def current_user(authorization: str = Header(default="")):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Autenticación requerida")
    try:
        return jwt.decode(authorization[7:], JWT_SECRET, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
