import sqlite3
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator

from .database import get_connection
from .seguridad import obtener_admin_actual

router = APIRouter(prefix="/api/paquetes", tags=["paquetes"])


class PaqueteCreate(BaseModel):
    nombre: str = Field(min_length=1)
    fecha_salida: date
    fecha_regreso: date
    cupo_maximo: int = Field(gt=0)
    margen: float = Field(default=0.20, ge=0)
    destino_ids: list[int] = Field(min_length=2, max_length=5)

    @field_validator("destino_ids")
    @classmethod
    def sin_destinos_repetidos(cls, v: list[int]) -> list[int]:
        if len(set(v)) != len(v):
            raise ValueError("Un paquete no puede repetir el mismo destino")
        return v

    @field_validator("fecha_regreso")
    @classmethod
    def regreso_posterior_a_salida(cls, v: date, info):
        salida = info.data.get("fecha_salida")
        if salida is not None and v <= salida:
            raise ValueError("La fecha de regreso debe ser posterior a la fecha de salida")
        return v


class DestinoResumen(BaseModel):
    id: int
    nombre: str
    costo_base: int


class Paquete(BaseModel):
    id: int
    nombre: str
    fecha_salida: date
    fecha_regreso: date
    cupo_maximo: int
    margen: float
    publicado: bool
    precio: int
    cupo_disponible: int
    destinos: list[DestinoResumen]


def _calcular_precio(destinos: list[sqlite3.Row], margen: float) -> int:
    """R6: precio = suma de costos base de los destinos incluidos, más el margen."""
    suma_costos = sum(d["costo_base"] for d in destinos)
    return round(suma_costos * (1 + margen))


def _cargar_paquete(conn: sqlite3.Connection, paquete_id: int) -> Paquete | None:
    row = conn.execute("SELECT * FROM paquetes WHERE id = ?", (paquete_id,)).fetchone()
    if row is None:
        return None

    destinos = conn.execute(
        "SELECT d.id, d.nombre, d.costo_base FROM destinos d "
        "JOIN paquete_destinos pd ON pd.destino_id = d.id "
        "WHERE pd.paquete_id = ? ORDER BY d.nombre",
        (paquete_id,),
    ).fetchall()

    reservado = conn.execute(
        "SELECT COALESCE(SUM(personas), 0) AS total FROM reservas WHERE paquete_id = ?",
        (paquete_id,),
    ).fetchone()["total"]

    # R7: publicado usa el precio fijado; sin publicar se calcula con los costos actuales.
    precio = row["precio_publicado"] if row["publicado"] else _calcular_precio(destinos, row["margen"])

    return Paquete(
        id=row["id"],
        nombre=row["nombre"],
        fecha_salida=date.fromisoformat(row["fecha_salida"]),
        fecha_regreso=date.fromisoformat(row["fecha_regreso"]),
        cupo_maximo=row["cupo_maximo"],
        margen=row["margen"],
        publicado=bool(row["publicado"]),
        precio=precio,
        cupo_disponible=row["cupo_maximo"] - reservado,
        destinos=[DestinoResumen(id=d["id"], nombre=d["nombre"], costo_base=d["costo_base"]) for d in destinos],
    )


def _validar_destinos_disponibles(conn: sqlite3.Connection, destino_ids: list[int]) -> None:
    ids_unicos = set(destino_ids)
    placeholders = ",".join("?" * len(ids_unicos))
    filas = conn.execute(
        f"SELECT id, disponible FROM destinos WHERE id IN ({placeholders})", list(ids_unicos)
    ).fetchall()

    encontrados = {f["id"] for f in filas}
    faltantes = ids_unicos - encontrados
    if faltantes:
        raise HTTPException(status_code=404, detail=f"Destino(s) inexistente(s): {sorted(faltantes)}")

    no_disponibles = sorted(f["id"] for f in filas if not f["disponible"])
    if no_disponibles:
        raise HTTPException(
            status_code=409,
            detail=f"Destino(s) no disponible(s) para armar paquetes nuevos: {no_disponibles}",
        )


@router.get("", response_model=list[Paquete])
def listar_paquetes():
    conn = get_connection()
    try:
        ids = [r["id"] for r in conn.execute("SELECT id FROM paquetes ORDER BY id").fetchall()]
        return [_cargar_paquete(conn, i) for i in ids]
    finally:
        conn.close()


@router.get("/{paquete_id}", response_model=Paquete)
def obtener_paquete(paquete_id: int):
    conn = get_connection()
    try:
        paquete = _cargar_paquete(conn, paquete_id)
        if paquete is None:
            raise HTTPException(status_code=404, detail="Paquete no encontrado")
        return paquete
    finally:
        conn.close()


@router.post("", response_model=Paquete, status_code=201)
def crear_paquete(datos: PaqueteCreate, _admin: str = Depends(obtener_admin_actual)):
    conn = get_connection()
    try:
        _validar_destinos_disponibles(conn, datos.destino_ids)
        try:
            cursor = conn.execute(
                "INSERT INTO paquetes (nombre, fecha_salida, fecha_regreso, cupo_maximo, margen) "
                "VALUES (?, ?, ?, ?, ?)",
                (
                    datos.nombre,
                    datos.fecha_salida.isoformat(),
                    datos.fecha_regreso.isoformat(),
                    datos.cupo_maximo,
                    datos.margen,
                ),
            )
            paquete_id = cursor.lastrowid
            conn.executemany(
                "INSERT INTO paquete_destinos (paquete_id, destino_id) VALUES (?, ?)",
                [(paquete_id, destino_id) for destino_id in datos.destino_ids],
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.rollback()
            raise HTTPException(status_code=400, detail="No se pudo crear el paquete: datos inválidos")
        return _cargar_paquete(conn, paquete_id)
    finally:
        conn.close()


@router.post("/{paquete_id}/publicar", response_model=Paquete)
def publicar_paquete(paquete_id: int, _admin: str = Depends(obtener_admin_actual)):
    """R7: el precio se calcula y queda fijado en el momento de publicar."""
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM paquetes WHERE id = ?", (paquete_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Paquete no encontrado")
        if row["publicado"]:
            raise HTTPException(status_code=409, detail="El paquete ya está publicado")

        destinos = conn.execute(
            "SELECT d.id, d.nombre, d.costo_base FROM destinos d "
            "JOIN paquete_destinos pd ON pd.destino_id = d.id "
            "WHERE pd.paquete_id = ?",
            (paquete_id,),
        ).fetchall()
        precio = _calcular_precio(destinos, row["margen"])

        conn.execute(
            "UPDATE paquetes SET publicado = 1, precio_publicado = ? WHERE id = ?",
            (precio, paquete_id),
        )
        conn.commit()
        return _cargar_paquete(conn, paquete_id)
    finally:
        conn.close()
