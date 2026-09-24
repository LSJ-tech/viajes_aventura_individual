from conftest import crear_destino, crear_paquete


def _dos_destinos(client, admin_headers, costo1=100000, costo2=50000):
    d1 = crear_destino(client, admin_headers, nombre="D1", costo_base=costo1)
    d2 = crear_destino(client, admin_headers, nombre="D2", costo_base=costo2)
    return d1, d2


def test_r3_minimo_dos_destinos(client, admin_headers):
    d1, _ = _dos_destinos(client, admin_headers)
    res = client.post(
        "/api/paquetes",
        json={
            "nombre": "Malo",
            "fecha_salida": "2026-10-01",
            "fecha_regreso": "2026-10-05",
            "cupo_maximo": 5,
            "destino_ids": [d1["id"]],
        },
        headers=admin_headers,
    )
    assert res.status_code == 422


def test_r3_maximo_cinco_destinos(client, admin_headers):
    ids = [crear_destino(client, admin_headers, nombre=f"D{i}")["id"] for i in range(6)]
    res = client.post(
        "/api/paquetes",
        json={
            "nombre": "Malo",
            "fecha_salida": "2026-10-01",
            "fecha_regreso": "2026-10-05",
            "cupo_maximo": 5,
            "destino_ids": ids,
        },
        headers=admin_headers,
    )
    assert res.status_code == 422


def test_r3_no_admite_destino_repetido(client, admin_headers):
    d1, _ = _dos_destinos(client, admin_headers)
    res = client.post(
        "/api/paquetes",
        json={
            "nombre": "Malo",
            "fecha_salida": "2026-10-01",
            "fecha_regreso": "2026-10-05",
            "cupo_maximo": 5,
            "destino_ids": [d1["id"], d1["id"]],
        },
        headers=admin_headers,
    )
    assert res.status_code == 422


def test_r5_fecha_regreso_posterior_a_salida(client, admin_headers):
    d1, d2 = _dos_destinos(client, admin_headers)
    res = client.post(
        "/api/paquetes",
        json={
            "nombre": "Malo",
            "fecha_salida": "2026-10-05",
            "fecha_regreso": "2026-10-01",
            "cupo_maximo": 5,
            "destino_ids": [d1["id"], d2["id"]],
        },
        headers=admin_headers,
    )
    assert res.status_code == 422


def test_r5_cupo_maximo_mayor_que_cero(client, admin_headers):
    d1, d2 = _dos_destinos(client, admin_headers)
    res = client.post(
        "/api/paquetes",
        json={
            "nombre": "Malo",
            "fecha_salida": "2026-10-01",
            "fecha_regreso": "2026-10-05",
            "cupo_maximo": 0,
            "destino_ids": [d1["id"], d2["id"]],
        },
        headers=admin_headers,
    )
    assert res.status_code == 422


def test_r6_precio_es_suma_de_costos_mas_margen(client, admin_headers):
    d1, d2 = _dos_destinos(client, admin_headers, costo1=100000, costo2=50000)
    paquete = crear_paquete(client, admin_headers, [d1["id"], d2["id"]], margen=0.20)
    assert paquete["precio"] == 180000  # (100000 + 50000) * 1.20


def test_no_se_puede_armar_con_un_destino_no_disponible(client, admin_headers):
    d1, d2 = _dos_destinos(client, admin_headers)
    d3 = crear_destino(client, admin_headers, nombre="D3")
    d4 = crear_destino(client, admin_headers, nombre="D4")
    crear_paquete(client, admin_headers, [d3["id"], d4["id"]])
    client.delete(f"/api/destinos/{d3['id']}", headers=admin_headers)  # queda no disponible (R8)

    res = client.post(
        "/api/paquetes",
        json={
            "nombre": "Malo",
            "fecha_salida": "2026-10-01",
            "fecha_regreso": "2026-10-05",
            "cupo_maximo": 5,
            "destino_ids": [d1["id"], d3["id"]],
        },
        headers=admin_headers,
    )
    assert res.status_code == 409


def test_r7_precio_publicado_no_cambia_si_cambia_el_costo_del_destino(client, admin_headers):
    d1, d2 = _dos_destinos(client, admin_headers, costo1=100000, costo2=50000)
    paquete = crear_paquete(client, admin_headers, [d1["id"], d2["id"]], margen=0.20)

    publicado = client.post(f"/api/paquetes/{paquete['id']}/publicar", headers=admin_headers).json()
    assert publicado["publicado"] is True
    assert publicado["precio"] == 180000

    client.put(
        f"/api/destinos/{d1['id']}",
        json={"nombre": "D1", "zona": "Z", "descripcion": "D", "duracion_dias": 2, "costo_base": 999999},
        headers=admin_headers,
    )

    tras_cambio = client.get(f"/api/paquetes/{paquete['id']}").json()
    assert tras_cambio["precio"] == 180000


def test_r7_no_se_puede_publicar_dos_veces(client, admin_headers):
    d1, d2 = _dos_destinos(client, admin_headers)
    paquete = crear_paquete(client, admin_headers, [d1["id"], d2["id"]])
    client.post(f"/api/paquetes/{paquete['id']}/publicar", headers=admin_headers)
    res = client.post(f"/api/paquetes/{paquete['id']}/publicar", headers=admin_headers)
    assert res.status_code == 409


def test_crear_y_publicar_requieren_sesion_de_administrador(client, admin_headers):
    d1, d2 = _dos_destinos(client, admin_headers)
    res = client.post(
        "/api/paquetes",
        json={
            "nombre": "Malo",
            "fecha_salida": "2026-10-01",
            "fecha_regreso": "2026-10-05",
            "cupo_maximo": 5,
            "destino_ids": [d1["id"], d2["id"]],
        },
    )
    assert res.status_code == 401
