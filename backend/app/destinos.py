import sqlite3

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from .database import get_connection
from .seguridad import obtener_admin_actual

router = APIRouter(prefix="/api/destinos", tags=["destinos"])


class DestinoDatos(BaseModel):
    nombre: str = Field(min_length=1)
    zona: str = Field(min_length=1)
    descripcion: str = Field(min_length=1)
    duracion_dias: int = Field(gt=0)
    costo_base: int = Field(gt=0)


class Destino(DestinoDatos):
    id: int
    disponible: bool


def _row_to_destino(row: sqlite3.Row) -> Destino:
    return Destino(
        id=row["id"],
        nombre=row["nombre"],
        zona=row["zona"],
        descripcion=row["descripcion"],
        duracion_dias=row["duracion_dias"],
        costo_base=row["costo_base"],
        disponible=bool(row["disponible"]),
    )


@router.get("", response_model=list[Destino])
def listar_destinos(solo_disponibles: bool = False):
    conn = get_connection()
    try:
        query = "SELECT * FROM destinos"
        if solo_disponibles:
            query += " WHERE disponible = 1"
        query += " ORDER BY nombre"
        rows = conn.execute(query).fetchall()
        return [_row_to_destino(r) for r in rows]
    finally:
        conn.close()


@router.get("/{destino_id}", response_model=Destino)
def obtener_destino(destino_id: int):
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM destinos WHERE id = ?", (destino_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Destino no encontrado")
        return _row_to_destino(row)
    finally:
        conn.close()


@router.post("", response_model=Destino, status_code=201)
def crear_destino(datos: DestinoDatos, _admin: str = Depends(obtener_admin_actual)):
    conn = get_connection()
    try:
        try:
            cursor = conn.execute(
                "INSERT INTO destinos (nombre, zona, descripcion, duracion_dias, costo_base) "
                "VALUES (?, ?, ?, ?, ?)",
                (datos.nombre, datos.zona, datos.descripcion, datos.duracion_dias, datos.costo_base),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=409, detail="Ya existe un destino con ese nombre")
        row = conn.execute("SELECT * FROM destinos WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return _row_to_destino(row)
    finally:
        conn.close()


@router.put("/{destino_id}", response_model=Destino)
def actualizar_destino(destino_id: int, datos: DestinoDatos, _admin: str = Depends(obtener_admin_actual)):
    conn = get_connection()
    try:
        actual = conn.execute("SELECT * FROM destinos WHERE id = ?", (destino_id,)).fetchone()
        if actual is None:
            raise HTTPException(status_code=404, detail="Destino no encontrado")
        try:
            conn.execute(
                "UPDATE destinos SET nombre = ?, zona = ?, descripcion = ?, duracion_dias = ?, costo_base = ? "
                "WHERE id = ?",
                (datos.nombre, datos.zona, datos.descripcion, datos.duracion_dias, datos.costo_base, destino_id),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=409, detail="Ya existe un destino con ese nombre")
        row = conn.execute("SELECT * FROM destinos WHERE id = ?", (destino_id,)).fetchone()
        return _row_to_destino(row)
    finally:
        conn.close()


@router.delete("/{destino_id}", response_model=Destino)
def eliminar_destino(destino_id: int, _admin: str = Depends(obtener_admin_actual)):
    """R8: sin paquetes asociados se elimina; con paquetes asociados se marca no disponible."""
    conn = get_connection()
    try:
        actual = conn.execute("SELECT * FROM destinos WHERE id = ?", (destino_id,)).fetchone()
        if actual is None:
            raise HTTPException(status_code=404, detail="Destino no encontrado")

        en_uso = conn.execute(
            "SELECT 1 FROM paquete_destinos WHERE destino_id = ?", (destino_id,)
        ).fetchone()

        if en_uso:
            conn.execute("UPDATE destinos SET disponible = 0 WHERE id = ?", (destino_id,))
            conn.commit()
            row = conn.execute("SELECT * FROM destinos WHERE id = ?", (destino_id,)).fetchone()
            return _row_to_destino(row)

        conn.execute("DELETE FROM destinos WHERE id = ?", (destino_id,))
        conn.commit()
        return _row_to_destino(actual)
    finally:
        conn.close()
