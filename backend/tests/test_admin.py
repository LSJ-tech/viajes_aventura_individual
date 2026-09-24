from conftest import registrar_cliente


def test_login_admin_correcto(client):
    res = client.post("/api/admin/login", json={"correo": "admin@test.cl", "password": "adminClave123"})
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_admin_password_incorrecta(client):
    res = client.post("/api/admin/login", json={"correo": "admin@test.cl", "password": "incorrecta"})
    assert res.status_code == 401


def test_login_admin_correo_incorrecto(client):
    res = client.post("/api/admin/login", json={"correo": "otro@test.cl", "password": "adminClave123"})
    assert res.status_code == 401


def test_token_de_cliente_no_sirve_como_admin(client):
    cliente = registrar_cliente(client)
    headers = {"Authorization": f"Bearer {cliente['access_token']}"}
    res = client.post(
        "/api/destinos",
        json={"nombre": "X", "zona": "Z", "descripcion": "D", "duracion_dias": 1, "costo_base": 1000},
        headers=headers,
    )
    assert res.status_code == 403


def test_token_de_admin_no_sirve_como_cliente(client, admin_headers):
    res = client.get("/api/clientes/me", headers=admin_headers)
    assert res.status_code == 403
