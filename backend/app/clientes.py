import sqlite3
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator

from .database import get_connection
from .seguridad import crear_token, hash_password, obtener_cliente_actual, verificar_password

router = APIRouter(prefix="/api/clientes", tags=["clientes"])

ClienteActual = Annotated[int, Depends(obtener_cliente_actual)]


def _rut_valido(rut: str) -> bool:
    """Verifica formato y dígito verificador de un RUT chileno (módulo 11)."""
    limpio = rut.upper().replace(".", "").replace("-", "")
    if len(limpio) < 2 or not limpio[:-1].isdigit():
        return False

    cuerpo, dv = limpio[:-1], limpio[-1]
    suma, factor = 0, 2
    for digito in reversed(cuerpo):
        suma += int(digito) * factor
        factor = 2 if factor == 7 else factor + 1

    resto = 11 - (suma % 11)
    dv_esperado = {11: "0", 10: "K"}.get(resto, str(resto))
    return dv == dv_esperado


class ClienteRegistro(BaseModel):
    nombre: str = Field(min_length=1)
    rut: str = Field(min_length=3)
    correo: EmailStr
    telefono: str = Field(min_length=1)
    password: str = Field(min_length=8, max_length=72)

    @field_validator("rut")
    @classmethod
    def rut_con_digito_verificador_valido(cls, v: str) -> str:
        if not _rut_valido(v):
            raise ValueError("RUT inválido")
        return v


class ClienteLogin(BaseModel):
    correo: EmailStr
    password: str


class ClientePerfil(BaseModel):
    """R17: nunca incluye rut ni teléfono, ni siquiera en el propio perfil."""

    id: int
    nombre: str
    correo: str


class TokenRespuesta(BaseModel):
    access_token: str
    token_type: str = "bearer"
    cliente: ClientePerfil


def _perfil(row: sqlite3.Row) -> ClientePerfil:
    return ClientePerfil(id=row["id"], nombre=row["nombre"], correo=row["correo"])


@router.post(
    "/registro",
    response_model=TokenRespuesta,
    status_code=201,
    responses={409: {"description": "Ya existe una cuenta con ese correo"}},
)
def registrar_cliente(datos: ClienteRegistro):
    conn = get_connection()
    try:
        try:
            cursor = conn.execute(
                "INSERT INTO clientes (nombre, rut, correo, telefono, password_hash) VALUES (?, ?, ?, ?, ?)",
                (datos.nombre, datos.rut, datos.correo, datos.telefono, hash_password(datos.password)),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=409, detail="Ya existe una cuenta con ese correo")

        row = conn.execute(
            "SELECT id, nombre, correo FROM clientes WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        return TokenRespuesta(access_token=crear_token(row["id"], "cliente"), cliente=_perfil(row))
    finally:
        conn.close()


@router.post(
    "/login",
    response_model=TokenRespuesta,
    responses={401: {"description": "Correo o contraseña incorrectos"}},
)
def iniciar_sesion(datos: ClienteLogin):
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT id, nombre, correo, password_hash FROM clientes WHERE correo = ?", (datos.correo,)
        ).fetchone()
        if row is None or not verificar_password(datos.password, row["password_hash"]):
            raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

        return TokenRespuesta(access_token=crear_token(row["id"], "cliente"), cliente=_perfil(row))
    finally:
        conn.close()


@router.get("/me", response_model=ClientePerfil)
def perfil_propio(cliente_id: ClienteActual):
    """R11: solo el propio cliente autenticado puede consultar su perfil."""
    conn = get_connection()
    try:
        row = conn.execute("SELECT id, nombre, correo FROM clientes WHERE id = ?", (cliente_id,)).fetchone()
        return _perfil(row)
    finally:
        conn.close()
