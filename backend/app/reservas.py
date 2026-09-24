import sqlite3
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from .database import get_connection
from .seguridad import obtener_cliente_actual

router = APIRouter(prefix="/api/reservas", tags=["reservas"])


class ReservaCreate(BaseModel):
    paquete_id: int
    personas: int = Field(ge=1)  # R16


class PaqueteResumen(BaseModel):
    id: int
    nombre: str
    fecha_salida: date
    fecha_regreso: date


class Reserva(BaseModel):
    id: int
    paquete: PaqueteResumen
    fecha_emision: date
    personas: int
    total: int


def _cargar_reserva(conn: sqlite3.Connection, reserva_id: int) -> Reserva:
    row = conn.execute(
        "SELECT r.id, r.fecha_emision, r.personas, r.total, "
        "p.id AS paquete_id, p.nombre AS paquete_nombre, p.fecha_salida, p.fecha_regreso "
        "FROM reservas r JOIN paquetes p ON p.id = r.paquete_id "
        "WHERE r.id = ?",
        (reserva_id,),
    ).fetchone()
    return Reserva(
        id=row["id"],
        paquete=PaqueteResumen(
            id=row["paquete_id"],
            nombre=row["paquete_nombre"],
            fecha_salida=date.fromisoformat(row["fecha_salida"]),
            fecha_regreso=date.fromisoformat(row["fecha_regreso"]),
        ),
        fecha_emision=date.fromisoformat(row["fecha_emision"]),
        personas=row["personas"],
        total=row["total"],
    )


@router.get("", response_model=list[Reserva])
def listar_mis_reservas(cliente_id: int = Depends(obtener_cliente_actual)):
    """R11: cada cliente ve únicamente sus propias reservas."""
    conn = get_connection()
    try:
        ids = [
            r["id"]
            for r in conn.execute(
                "SELECT id FROM reservas WHERE cliente_id = ? ORDER BY fecha_emision DESC, id DESC",
                (cliente_id,),
            ).fetchall()
        ]
        return [_cargar_reserva(conn, i) for i in ids]
    finally:
        conn.close()


@router.post("", response_model=Reserva, status_code=201)
def crear_reserva(datos: ReservaCreate, cliente_id: int = Depends(obtener_cliente_actual)):
    conn = get_connection()
    try:
        paquete = conn.execute("SELECT * FROM paquetes WHERE id = ?", (datos.paquete_id,)).fetchone()
        if paquete is None:
            raise HTTPException(status_code=404, detail="Paquete no encontrado")

        # Supuesto: solo se reservan paquetes publicados (README §5); antes de
        # publicarse el precio aún no está fijado (R7) y el paquete es un borrador.
        if not paquete["publicado"]:
            raise HTTPException(status_code=409, detail="El paquete todavía no está publicado")

        # R15: no se acepta una reserva sobre un paquete cuya fecha de salida ya pasó.
        if date.fromisoformat(paquete["fecha_salida"]) < date.today():
            raise HTTPException(
                status_code=409, detail="No se puede reservar un paquete cuya fecha de salida ya pasó"
            )

        # R14: cupo disponible = cupo máximo - personas ya reservadas.
        reservado = conn.execute(
            "SELECT COALESCE(SUM(personas), 0) AS total FROM reservas WHERE paquete_id = ?",
            (datos.paquete_id,),
        ).fetchone()["total"]
        cupo_disponible = paquete["cupo_maximo"] - reservado
        if datos.personas > cupo_disponible:
            raise HTTPException(
                status_code=409,
                detail=f"No hay cupo suficiente: quedan {cupo_disponible} lugar(es) disponibles",
            )

        # R13: el total se calcula ahora, con el precio ya fijado, y no vuelve a cambiar.
        total = paquete["precio_publicado"] * datos.personas

        cursor = conn.execute(
            "INSERT INTO reservas (cliente_id, paquete_id, fecha_emision, personas, total) "
            "VALUES (?, ?, ?, ?, ?)",
            (cliente_id, datos.paquete_id, date.today().isoformat(), datos.personas, total),
        )
        conn.commit()
        return _cargar_reserva(conn, cursor.lastrowid)
    finally:
        conn.close()
