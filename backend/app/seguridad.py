import os
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .database import get_connection

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "clave-de-desarrollo-cambiar-en-produccion")
ALGORITMO = "HS256"
EXPIRACION_MINUTOS = 60 * 12

# El caso describe un único administrador (uno de los socios, ver Viajes_aventura.pdf
# §1.3), no una tabla de administradores: sus credenciales se configuran por variable
# de entorno en vez de guardarse en la base de datos.
ADMIN_CORREO = os.environ.get("ADMIN_EMAIL", "admin@viajesaventura.cl")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "cambiar-esta-clave-en-produccion")

_bearer = HTTPBearer()


def hash_password(password: str) -> str:
    """R10: la contraseña nunca se guarda tal como el cliente la escribió."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def verificar_credenciales_admin(correo: str, password: str) -> bool:
    correo_ok = secrets.compare_digest(correo.strip().lower(), ADMIN_CORREO.strip().lower())
    password_ok = secrets.compare_digest(password, ADMIN_PASSWORD)
    return correo_ok and password_ok


def crear_token(sujeto: int | str, rol: str) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=EXPIRACION_MINUTOS)
    payload = {"sub": str(sujeto), "rol": rol, "exp": expira}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITMO)


def _decodificar(credenciales: HTTPAuthorizationCredentials) -> dict:
    try:
        return jwt.decode(credenciales.credentials, SECRET_KEY, algorithms=[ALGORITMO])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


def obtener_cliente_actual(credenciales: HTTPAuthorizationCredentials = Depends(_bearer)) -> int:
    """R11: valida el JWT recibido y devuelve el id del cliente autenticado."""
    payload = _decodificar(credenciales)
    if payload.get("rol") != "cliente":
        raise HTTPException(status_code=403, detail="Se requiere una sesión de cliente")
    try:
        cliente_id = int(payload["sub"])
    except (KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    conn = get_connection()
    try:
        existe = conn.execute("SELECT 1 FROM clientes WHERE id = ?", (cliente_id,)).fetchone()
    finally:
        conn.close()
    if existe is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    return cliente_id


def obtener_admin_actual(credenciales: HTTPAuthorizationCredentials = Depends(_bearer)) -> str:
    """Protege las operaciones de administración del catálogo (crear/editar destinos y paquetes)."""
    payload = _decodificar(credenciales)
    if payload.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="Se requiere una sesión de administrador")
    return payload["sub"]
