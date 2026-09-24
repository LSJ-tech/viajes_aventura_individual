import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "viajes_aventura.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS destinos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    zona TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    duracion_dias INTEGER NOT NULL CHECK (duracion_dias > 0),
    costo_base INTEGER NOT NULL CHECK (costo_base > 0),
    disponible INTEGER NOT NULL DEFAULT 1 CHECK (disponible IN (0, 1))
);

CREATE TABLE IF NOT EXISTS paquetes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    fecha_salida TEXT NOT NULL,
    fecha_regreso TEXT NOT NULL,
    cupo_maximo INTEGER NOT NULL CHECK (cupo_maximo > 0),
    margen REAL NOT NULL DEFAULT 0.20 CHECK (margen >= 0),
    precio_publicado INTEGER,
    publicado INTEGER NOT NULL DEFAULT 0 CHECK (publicado IN (0, 1)),
    CHECK (fecha_regreso > fecha_salida)
);

CREATE TABLE IF NOT EXISTS paquete_destinos (
    paquete_id INTEGER NOT NULL REFERENCES paquetes(id),
    destino_id INTEGER NOT NULL REFERENCES destinos(id),
    PRIMARY KEY (paquete_id, destino_id)
);

CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    rut TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE,
    telefono TEXT NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id),
    paquete_id INTEGER NOT NULL REFERENCES paquetes(id),
    fecha_emision TEXT NOT NULL,
    personas INTEGER NOT NULL CHECK (personas >= 1),
    total INTEGER NOT NULL
);
"""


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()
