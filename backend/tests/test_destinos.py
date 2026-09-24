from conftest import crear_destino, crear_paquete


def test_r1_nombre_no_se_repite_en_el_catalogo(client, admin_headers):
    crear_destino(client, admin_headers, nombre="Valle del Elqui")
    res = client.post(
        "/api/destinos",
        json={
            "nombre": "Valle del Elqui",
            "zona": "Coquimbo",
            "descripcion": "Otra descripción",
            "duracion_dias": 2,
            "costo_base": 120000,
        },
        headers=admin_headers,
    )
    assert res.status_code == 409


def test_r1_campos_obligatorios(client, admin_headers):
    res = client.post(
        "/api/destinos",
        json={"nombre": "", "zona": "Z", "descripcion": "D", "duracion_dias": 1, "costo_base": 1000},
        headers=admin_headers,
    )
    assert res.status_code == 422


def test_r2_costo_base_mayor_que_cero(client, admin_headers):
    res = client.post(
        "/api/destinos",
        json={"nombre": "X", "zona": "Z", "descripcion": "D", "duracion_dias": 1, "costo_base": 0},
        headers=admin_headers,
    )
    assert res.status_code == 422


def test_r8_destino_sin_paquetes_se_elimina(client, admin_headers):
    d = crear_destino(client, admin_headers)
    res = client.delete(f"/api/destinos/{d['id']}", headers=admin_headers)
    assert res.status_code == 200
    assert client.get("/api/destinos").json() == []


def test_r8_destino_en_uso_se_marca_no_disponible_en_vez_de_borrarse(client, admin_headers):
    d1 = crear_destino(client, admin_headers, nombre="D1")
    d2 = crear_destino(client, admin_headers, nombre="D2")
    crear_paquete(client, admin_headers, [d1["id"], d2["id"]])

    res = client.delete(f"/api/destinos/{d1['id']}", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["disponible"] is False

    listado = client.get("/api/destinos").json()
    assert any(d["id"] == d1["id"] and d["disponible"] is False for d in listado)


def test_escritura_requiere_sesion_de_administrador(client):
    res = client.post(
        "/api/destinos",
        json={"nombre": "X", "zona": "Z", "descripcion": "D", "duracion_dias": 1, "costo_base": 1000},
    )
    assert res.status_code == 401


def test_lectura_del_catalogo_es_publica(client, admin_headers):
    crear_destino(client, admin_headers)
    res = client.get("/api/destinos")
    assert res.status_code == 200
    assert len(res.json()) == 1
