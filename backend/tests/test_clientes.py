from app import database

from conftest import registrar_cliente


def test_r9_registro_devuelve_token_y_perfil(client):
    data = registrar_cliente(client)
    assert "access_token" in data
    assert data["cliente"]["correo"] == "cliente@test.cl"


def test_r9_correo_no_se_repite(client):
    registrar_cliente(client, correo="dup@test.cl")
    res = client.post(
        "/api/clientes/registro",
        json={
            "nombre": "Otro",
            "rut": "9668077-5",
            "correo": "dup@test.cl",
            "telefono": "+56911111111",
            "password": "otraClave123",
        },
    )
    assert res.status_code == 409


def test_r9_rut_con_digito_verificador_invalido(client):
    res = client.post(
        "/api/clientes/registro",
        json={
            "nombre": "Malo",
            "rut": "12345678-0",
            "correo": "malo@test.cl",
            "telefono": "+56900000000",
            "password": "claveSegura123",
        },
    )
    assert res.status_code == 422


def test_r10_password_se_guarda_hasheada(client, monkeypatch):
    registrar_cliente(client)
    conn = database.get_connection()
    try:
        fila = conn.execute("SELECT password_hash FROM clientes WHERE correo = ?", ("cliente@test.cl",)).fetchone()
    finally:
        conn.close()
    assert fila["password_hash"] != "claveSegura123"
    assert fila["password_hash"].startswith("$2b$")  # prefijo estándar de un hash bcrypt


def test_login_correcto_devuelve_token(client):
    registrar_cliente(client)
    res = client.post("/api/clientes/login", json={"correo": "cliente@test.cl", "password": "claveSegura123"})
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_password_incorrecta(client):
    registrar_cliente(client)
    res = client.post("/api/clientes/login", json={"correo": "cliente@test.cl", "password": "incorrecta"})
    assert res.status_code == 401


def test_r11_me_requiere_token(client):
    assert client.get("/api/clientes/me").status_code == 401


def test_r17_rut_y_telefono_nunca_se_devuelven(client):
    data = registrar_cliente(client)
    assert "rut" not in data["cliente"]
    assert "telefono" not in data["cliente"]

    headers = {"Authorization": f"Bearer {data['access_token']}"}
    perfil = client.get("/api/clientes/me", headers=headers).json()
    assert "rut" not in perfil
    assert "telefono" not in perfil
