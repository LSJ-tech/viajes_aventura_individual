import threading

from conftest import cliente_headers, crear_destino, crear_paquete, registrar_cliente


def _paquete_publicado(client, admin_headers, cupo_maximo=10, fecha_salida="2026-10-01", margen=0.20):
    d1 = crear_destino(client, admin_headers, nombre="D1", costo_base=100000)
    d2 = crear_destino(client, admin_headers, nombre="D2", costo_base=50000)
    paquete = crear_paquete(
        client,
        admin_headers,
        [d1["id"], d2["id"]],
        cupo_maximo=cupo_maximo,
        fecha_salida=fecha_salida,
        fecha_regreso="2026-12-31" if fecha_salida > "2020-01-01" else "2020-01-05",
        margen=margen,
    )
    return client.post(f"/api/paquetes/{paquete['id']}/publicar", headers=admin_headers).json()


def test_no_se_puede_reservar_un_paquete_sin_publicar(client, admin_headers):
    d1 = crear_destino(client, admin_headers, nombre="D1")
    d2 = crear_destino(client, admin_headers, nombre="D2")
    paquete = crear_paquete(client, admin_headers, [d1["id"], d2["id"]])
    headers = cliente_headers(client)

    res = client.post("/api/reservas", json={"paquete_id": paquete["id"], "personas": 1}, headers=headers)
    assert res.status_code == 409


def test_r12_r13_total_es_precio_por_personas_y_queda_fijo(client, admin_headers):
    paquete = _paquete_publicado(client, admin_headers)  # precio = 180000
    headers = cliente_headers(client)

    res = client.post("/api/reservas", json={"paquete_id": paquete["id"], "personas": 3}, headers=headers)
    assert res.status_code == 201
    reserva = res.json()
    assert reserva["total"] == 540000
    assert reserva["personas"] == 3
    assert reserva["paquete"]["id"] == paquete["id"]


def test_r14_no_se_acepta_reserva_que_supere_el_cupo(client, admin_headers):
    paquete = _paquete_publicado(client, admin_headers, cupo_maximo=3)
    headers = cliente_headers(client)

    ok = client.post("/api/reservas", json={"paquete_id": paquete["id"], "personas": 2}, headers=headers)
    assert ok.status_code == 201

    excede = client.post("/api/reservas", json={"paquete_id": paquete["id"], "personas": 2}, headers=headers)
    assert excede.status_code == 409

    justo = client.post("/api/reservas", json={"paquete_id": paquete["id"], "personas": 1}, headers=headers)
    assert justo.status_code == 201


def test_r15_no_se_acepta_reserva_con_fecha_de_salida_vencida(client, admin_headers):
    paquete = _paquete_publicado(client, admin_headers, fecha_salida="2020-01-01")
    headers = cliente_headers(client)

    res = client.post("/api/reservas", json={"paquete_id": paquete["id"], "personas": 1}, headers=headers)
    assert res.status_code == 409


def test_r16_personas_al_menos_uno(client, admin_headers):
    paquete = _paquete_publicado(client, admin_headers)
    headers = cliente_headers(client)

    res = client.post("/api/reservas", json={"paquete_id": paquete["id"], "personas": 0}, headers=headers)
    assert res.status_code == 422


def test_reservar_requiere_autenticacion(client, admin_headers):
    paquete = _paquete_publicado(client, admin_headers)
    res = client.post("/api/reservas", json={"paquete_id": paquete["id"], "personas": 1})
    assert res.status_code == 401


def test_r11_cada_cliente_ve_unicamente_sus_propias_reservas(client, admin_headers):
    paquete = _paquete_publicado(client, admin_headers, cupo_maximo=10)

    headers_a = cliente_headers(client, correo="a@test.cl")
    client.post("/api/reservas", json={"paquete_id": paquete["id"], "personas": 1}, headers=headers_a)

    headers_b = cliente_headers(client, correo="b@test.cl", rut="9668077-5")
    reservas_b = client.get("/api/reservas", headers=headers_b).json()
    assert reservas_b == []

    reservas_a = client.get("/api/reservas", headers=headers_a).json()
    assert len(reservas_a) == 1


def test_r14_dos_reservas_concurrentes_no_sobrevenden_el_cupo(client, admin_headers):
    """Regresión: sin el BEGIN IMMEDIATE, ambos hilos podían leer el mismo cupo
    disponible antes de que el otro insertara su reserva, y las dos pasaban."""
    paquete = _paquete_publicado(client, admin_headers, cupo_maximo=1)
    headers_a = cliente_headers(client, correo="carrera_a@test.cl")
    headers_b = cliente_headers(client, correo="carrera_b@test.cl", rut="9668077-5")

    codigos = {}

    def reservar(nombre, headers):
        res = client.post("/api/reservas", json={"paquete_id": paquete["id"], "personas": 1}, headers=headers)
        codigos[nombre] = res.status_code

    hilo_a = threading.Thread(target=reservar, args=("a", headers_a))
    hilo_b = threading.Thread(target=reservar, args=("b", headers_b))
    hilo_a.start()
    hilo_b.start()
    hilo_a.join()
    hilo_b.join()

    assert sorted(codigos.values()) == [201, 409]

    reservado_total = client.get(f"/api/paquetes/{paquete['id']}").json()["cupo_disponible"]
    assert reservado_total == 0
