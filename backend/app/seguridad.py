import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .database import get_connection

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "clave-de-desarrollo-cambiar-en-produccion")
ALGORITMO = "HS256"
EXPIRACION_MINUTOS = 60 * 12

_bearer = HTTPBearer()


def hash_password(password: str) -> str:
    """R10: la contraseña nunca se guarda tal como el cliente la escribió."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def crear_token(cliente_id: int) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=EXPIRACION_MINUTOS)
    payload = {"sub": str(cliente_id), "exp": expira}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITMO)


def obtener_cliente_actual(credenciales: HTTPAuthorizationCredentials = Depends(_bearer)) -> int:
    """R11: valida el JWT recibido y devuelve el id del cliente autenticado."""
    try:
        payload = jwt.decode(credenciales.credentials, SECRET_KEY, algorithms=[ALGORITMO])
        cliente_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    conn = get_connection()
    try:
        existe = conn.execute("SELECT 1 FROM clientes WHERE id = ?", (cliente_id,)).fetchone()
    finally:
        conn.close()
    if existe is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    return cliente_id
