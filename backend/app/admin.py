from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from .seguridad import crear_token, verificar_credenciales_admin

router = APIRouter(prefix="/api/admin", tags=["admin"])


class AdminLogin(BaseModel):
    correo: EmailStr
    password: str


class TokenAdmin(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post(
    "/login",
    response_model=TokenAdmin,
    responses={401: {"description": "Correo o contraseña incorrectos"}},
)
def iniciar_sesion_admin(datos: AdminLogin):
    if not verificar_credenciales_admin(datos.correo, datos.password):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    return TokenAdmin(access_token=crear_token(datos.correo, "admin"))
