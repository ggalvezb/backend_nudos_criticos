# routers/auth_user.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from db.client import db_client
from typing import List
import jwt, os, hashlib, hmac

router = APIRouter(prefix="/auth", tags=["Auth"])

registro_bd = db_client["monitor"]  # o "monitores"

JWT_SECRET = os.getenv("JWT_SECRET", "supersecreto")
JWT_ALG = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(plain: str, stored: str) -> bool:
    if not stored:
        return False
    if len(stored) == 64 and all(c in "0123456789abcdef" for c in stored.lower()):
        return hmac.compare_digest(hash_password(plain), stored)
    return hmac.compare_digest(plain, stored)

def create_token(sub: str, decretos: List[str], tipousuario: str, minutes: int = 240):
    now = datetime.utcnow()
    payload = {
      "sub": sub, "decretos": decretos, "tipousuario": tipousuario,
      "iat": now, "exp": now + timedelta(minutes=minutes),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        return {
            "username": payload["sub"],
            "decretos": payload.get("Decretos", []),
            "tipousuario": payload.get("Tipousuario", "")
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):  
    doc = registro_bd.find_one({"Usuario": form.username})
    print("Usuario buscado:", form.username)
    print("Documento encontrado:", doc) 
    if not doc or not verify_password(form.password, doc.get("Password", "")):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    username = doc.get("Usuario", form.username)
    decretos = doc.get("Decretos", [])
    tipousuario = doc.get("Tipousuario", "")

    token = create_token(username, decretos, tipousuario)
    return {
        "access_token": token,
        "token_type": "bearer",
        "tipousuario": tipousuario,
        "decretos": decretos
    }
