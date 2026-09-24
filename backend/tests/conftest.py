import os

# Deben quedar fijos antes de importar app.main: seguridad.py los lee como
# constantes de módulo (SECRET_KEY, ADMIN_CORREO, ADMIN_PASSWORD) al importarse.
os.environ.setdefault("JWT_SECRET_KEY", "clave-de-pruebas-de-al-menos-32-bytes-de-largo")
os.environ.setdefault("ADMIN_EMAIL", "admin@test.cl")
os.environ.setdefault("ADMIN_PASSWORD", "adminClave123")

import pytest
from fastapi.testclient import TestClient

from app import database
from app.main import app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    """Cada test corre contra una base SQLite temporal y aislada."""
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    database.init_db()
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def admin_headers(client):
    res = client.post("/api/admin/login", json={"correo": "admin@test.cl", "password": "adminClave123"})
    assert res.status_code == 200, res.text
    return {"Authorization": f"Bearer {res.json()['access_token']}"}


def crear_destino(client, admin_headers, **overrides):
    datos = {
        "nombre": "Destino genérico",
        "zona": "Zona",
        "descripcion": "Descripción",
        "duracion_dias": 2,
        "costo_base": 100000,
    }
    datos.update(overrides)
    res = client.post("/api/destinos", json=datos, headers=admin_headers)
    assert res.status_code == 201, res.text
    return res.json()


def crear_paquete(client, admin_headers, destino_ids, **overrides):
    datos = {
        "nombre": "Paquete genérico",
        "fecha_salida": "2026-10-01",
        "fecha_regreso": "2026-10-05",
        "cupo_maximo": 10,
        "margen": 0.20,
        "destino_ids": destino_ids,
    }
    datos.update(overrides)
    res = client.post("/api/paquetes", json=datos, headers=admin_headers)
    assert res.status_code == 201, res.text
    return res.json()


def registrar_cliente(client, **overrides):
    datos = {
        "nombre": "Cliente Test",
        "rut": "12345678-5",
        "correo": "cliente@test.cl",
        "telefono": "+56900000000",
        "password": "claveSegura123",
    }
    datos.update(overrides)
    res = client.post("/api/clientes/registro", json=datos)
    assert res.status_code == 201, res.text
    return res.json()


def cliente_headers(client, **overrides):
    data = registrar_cliente(client, **overrides)
    return {"Authorization": f"Bearer {data['access_token']}"}
