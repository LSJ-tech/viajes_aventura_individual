# Viajes Aventura — Sistema de gestión de agencia de viajes

Sistema web (**backend Python** + **frontend React**) para digitalizar la operación de **Viajes Aventura**, una agencia de viajes de Valparaíso que arma y vende paquetes turísticos combinando destinos. Reemplaza la planilla de cálculo, el cuaderno de reservas y las conversaciones de mensajería que hoy usan los tres socios para administrar destinos, paquetes, clientes y reservas.

Caso de estudio de la asignatura **TI3V21 Programación Orientada a Objeto Seguro** (INACAP Valparaíso), Unidad 4. Profesor: **Rubén Schnettler**. Autor: **Logan Silva Jara**.

| | |
|---|---|
| Backend | Python 3.10+ · **FastAPI** · `sqlite3` (librería estándar) |
| Frontend | **React** (consume el backend como API REST/JSON) |
| Fuente del caso | `Viajes_aventura.pdf` (antecedentes para el levantamiento de requerimientos) |
| Estado | Los 4 dominios implementados (R1-R17 completas), con rol de administrador, 43 pruebas automatizadas, modelo UML y SonarCloud sin hallazgos abiertos |
| Trazabilidad | `VALIDACION_IA.md`: bitácora de cambios apoyados por IA |

## Índice

1. [El negocio](#1-el-negocio)
2. [Cómo trabajan hoy (el problema)](#2-cómo-trabajan-hoy-el-problema)
3. [Reglas de negocio confirmadas](#3-reglas-de-negocio-confirmadas)
4. [Alcance del proyecto](#4-alcance-del-proyecto)
5. [Vacíos del caso y supuestos](#5-vacíos-del-caso-y-supuestos)
6. [Tecnología](#6-tecnología)
7. [Plan de trabajo](#7-plan-de-trabajo)
8. [Estado actual y próximos pasos](#8-estado-actual-y-próximos-pasos)
9. [Uso de IA y registro de cambios](#9-uso-de-ia-y-registro-de-cambios)

## 1. El negocio

Viajes Aventura es una agencia creada hace dos años por tres socios en Valparaíso (oficina en calle Esmeralda): Paulina Ovalle (catálogo y paquetes), Matías Bórquez (atención y reservas) e Ignacio Salas (administración y datos). No revenden paquetes de terceros: arman los suyos combinando destinos que ellos mismos han recorrido.

El ingreso proviene de la venta de paquetes a personas naturales, pagados por transferencia. El costo principal son los servicios contratados en cada destino (transporte, alojamiento, guías). Hoy no existe ningún sistema: todo vive en una planilla de cálculo, un cuaderno de reservas y conversaciones de mensajería.

**Cifras de la última temporada:** 18 destinos en catálogo (4 ya no se operan), entre 8 y 12 paquetes publicados por temporada, 214 reservas, 19 duplicadas al cierre, 6 aceptadas sobre el cupo del paquete, 3 sobre paquetes con fecha de salida vencida, 4 paquetes publicados con un precio distinto del cobrado, y 31 consultas de clientes resueltas revisando el cuaderno a mano.

## 2. Cómo trabajan hoy (el problema)

- **Catálogo de destinos**: planilla compartida editada por los tres socios. Hay destinos repetidos con nombres distintos, destinos que ya no se operan pero siguen apareciendo, y costos que nadie recuerda cuándo se actualizaron.
- **Armado de paquetes**: se buscan destinos y se suman costos a mano en otra hoja; la fórmula del precio a veces se rompe al copiar filas. Si se corrige el costo de un destino, los paquetes **ya vendidos** cambian de precio en la planilla, aunque el cliente haya pagado otro valor.
- **Reservas**: se anotan en un cuaderno y se confirman por mensajería. Los datos del cliente (nombre, RUT, teléfono, correo) quedan solo ahí y, a veces, solo en la conversación del socio que atendió. No hay forma confiable de saber cuántas personas han viajado con la agencia.
- **Cupos**: se llevan de cabeza y en el cuaderno; ya se vendieron más lugares que el cupo real de un paquete.
- **Fechas**: se ha vendido un paquete cuya fecha de salida ya había pasado, porque en la planilla se veía "disponible".

## 3. Reglas de negocio confirmadas

Confirmadas por los socios; son reglas de operación, **no** requerimientos — la traducción a requerimientos del sistema es parte del trabajo evaluado.

| # | Regla |
|---|---|
| R1 | Un destino tiene nombre, zona, descripción, duración en días y costo base por persona. El nombre no se repite en el catálogo. |
| R2 | El costo base de un destino es siempre mayor que cero. |
| R3 | Un paquete combina entre **dos y cinco** destinos, y ningún destino se repite dentro del mismo paquete. |
| R4 | Un mismo destino puede formar parte de varios paquetes al mismo tiempo. |
| R5 | Un paquete tiene nombre, fecha de salida, fecha de regreso y cupo máximo de personas. La fecha de regreso es posterior a la de salida y el cupo es mayor que cero. |
| R6 | Al crear un paquete, el administrador define sus fechas y su margen de operación (habitualmente 20 %, nunca negativo). El sistema **calcula** el precio por persona como la suma de los costos base de los destinos incluidos, más ese margen. |
| R7 | El precio queda fijado cuando el paquete se publica. Si después cambia el costo de un destino, los paquetes ya publicados conservan su precio. |
| R8 | Un destino que no forma parte de ningún paquete se elimina del catálogo. Si forma parte de alguno, no se elimina: se marca como **no disponible** y deja de ofrecerse para paquetes nuevos, conservando su contenido en los ya vendidos. |
| R9 | Un cliente se registra con nombre, RUT, correo electrónico, teléfono y contraseña. El correo identifica al cliente y no se repite. |
| R10 | La contraseña nunca se almacena tal como el cliente la escribió. |
| R11 | Solo un cliente autenticado puede reservar y consultar reservas, y cada cliente ve únicamente las suyas. |
| R12 | Una reserva corresponde a un cliente y a un paquete, y registra la fecha en que se emitió, la cantidad de personas y el total cobrado. |
| R13 | El total de una reserva se calcula al momento de reservar, multiplicando el precio del paquete por la cantidad de personas, y no vuelve a cambiar. |
| R14 | El cupo disponible de un paquete es su cupo máximo menos las personas ya reservadas. No se acepta una reserva que supere el cupo disponible. |
| R15 | No se acepta una reserva sobre un paquete cuya fecha de salida ya pasó. |
| R16 | La cantidad de personas de una reserva es al menos uno. |
| R17 | El RUT y el teléfono de un cliente son datos sensibles: no se muestran en listados ni en mensajes de error. |

## 4. Alcance del proyecto

**Dentro del alcance:**
- Destinos: registrar, modificar, dejar no disponible y listar los del catálogo.
- Paquetes: crear combinando destinos, definir fechas y cupo, calcular el precio y consultar disponibilidad.
- Reservas: registro y autenticación de clientes, reservar un paquete, almacenar la reserva y consultar el historial propio.
- Seguridad del sistema: autenticación, validación de todo dato ingresado y protección de credenciales y datos sensibles.

**Fuera del alcance:** pasarela de pago y verificación automática de transferencias · facturación electrónica ante el SII · aplicación para teléfonos · integración con aerolíneas, hoteles u operadores externos · envío de correos o mensajería al cliente · informes de gestión para los socios · contabilidad y remuneraciones.

## 5. Vacíos del caso y supuestos

El caso no entrega toda la información necesaria para implementar el sistema. Cuando un dato no estaba disponible, el criterio fue adoptar un supuesto explícito y fundamentarlo técnicamente, en vez de dejarlo implícito en el código. Estos son los supuestos adoptados (cada uno con el detalle técnico en el `Cambio` correspondiente de `VALIDACION_IA.md`):

| Vacío del caso | Supuesto adoptado | Fundamento |
|---|---|---|
| ¿Qué ocurre cuando un cliente desiste de una reserva? | No se implementa cancelación de reservas en esta versión. | El alcance (§4) define Reservas como "registro y autenticación de clientes, reservar un paquete, almacenar la reserva y consultar el historial propio" — cancelar no está entre esas funciones. |
| ¿Cómo se comporta un paquete cuando su "temporada" termina? | No existe un estado de "temporada terminada": R5 modela el paquete con `fecha_salida`/`fecha_regreso` concretas (no una temporada abstracta como "Julio" o "Todo el año"), y R15 ya impide reservar un paquete cuya `fecha_salida` ya pasó. | R5, R15 — Cambio 9. |
| ¿Quién puede modificar el catálogo? | Un único administrador (el caso describe un solo socio a cargo del catálogo, §1.3), autenticado por separado de los clientes. El catálogo de lectura (`GET`) sigue siendo público. | Cambio 10. |
| ¿Se puede reservar un paquete que aún no está publicado? | No: mientras no está publicado su precio no está fijado (R7) y es un borrador que el administrador puede seguir ajustando. | R7 — Cambio 9 (revisión técnica). |
| ¿Se puede editar o eliminar un paquete ya creado? | No: el alcance (§4) para Paquetes solo incluye crear, definir fechas/cupo, calcular el precio y consultar disponibilidad — no modificar ni eliminar. | Cambio 7 (revisión técnica). |
| ¿Qué formato debe tener el RUT? | Se valida formato y dígito verificador con el algoritmo módulo 11 estándar chileno. | R9 — Cambio 8. |
| ¿El catálogo de destinos y paquetes requiere sesión para consultarse? | No: el caso describe al cliente "consultando los paquetes disponibles" antes de registrarse (§1.3), así que el catálogo es público; solo reservar y ver el historial propio requieren sesión. | R11 — Cambios 9 y 10. |

## 6. Tecnología

Arquitectura de dos partes, separadas en carpetas propias dentro del repositorio:

- **Backend — `backend/app/`**: Python 3.10+ con **FastAPI**, expuesto como API REST/JSON. Se eligió sobre Flask porque valida automáticamente cada entrada con Pydantic (clave para las reglas R2, R5, R6, R16), genera documentación interactiva (`/docs`) útil para probar la API sin frontend, y su soporte async encaja con el modelo cliente-servidor separado del frontend. Persistencia con `sqlite3` de la librería estándar (`backend/app/database.py`, esquema de las 5 tablas con sus claves foráneas y `CHECK` de las reglas de negocio que se pueden expresar a nivel de columna); autenticación con JWT (`pyjwt`) y contraseñas hasheadas con `bcrypt` para cumplir R9-R11 y R17 (`backend/app/seguridad.py`, `backend/app/clientes.py`).
- **Frontend — `frontend/`**: **React + Vite**, consumiendo el backend únicamente vía HTTP/JSON (sin acceso directo a la base de datos). Pantallas para catálogo de destinos y paquetes (pública), registro/login/reservas de cliente (autenticada) y login de administrador.
- **Roles y autorización** (`backend/app/seguridad.py`, `backend/app/admin.py`): dos roles separados por el claim `rol` del JWT. **Cliente**: se registra vía `POST /api/clientes/registro`, solo puede reservar y ver sus propias reservas (R11). **Administrador**: único (el caso describe un solo socio a cargo, ver §1.3 de `Viajes_aventura.pdf`), inicia sesión en `POST /api/admin/login` con credenciales fijadas por variable de entorno (`ADMIN_EMAIL`, `ADMIN_PASSWORD` — no hay tabla de administradores), y es el único que puede crear/editar/eliminar destinos y crear/publicar paquetes. El catálogo (`GET /api/destinos`, `GET /api/paquetes`) sigue siendo público, sin autenticación.
- **Modelo UML**: diagrama de clases del dominio en [`docs/modelo-uml.md`](docs/modelo-uml.md), con la tabla de qué regla de negocio representa cada elemento.
- **Pruebas automatizadas** (`backend/tests/`, `pytest` + `TestClient` de FastAPI): 43 pruebas que cubren las 17 reglas de negocio, la separación de roles y una prueba de concurrencia (dos reservas simultáneas con `threading.Thread`) que confirma que el cupo de un paquete no se puede sobrevender (R14, protegido con una transacción `BEGIN IMMEDIATE` en `backend/app/reservas.py`), cada una contra una base SQLite temporal y aislada. Se corren con `cd backend && py -3 -m pip install -r requirements-dev.txt && py -3 -m pytest`.
- **Análisis estático** con [SonarCloud](https://sonarcloud.io/summary/overall?id=LSJ-tech_viajes_aventura_individual&branch=main) (análisis automático en cada push): Quality Gate en `OK`, 0 bugs, 0 vulnerabilidades, 0 code smells, 0 security hotspots.

**Cómo se ejecutan juntos:**
- **Durante el desarrollo**: dos procesos en paralelo.
  - Backend: `cd backend && py -3 -m pip install -r requirements.txt && py -3 -m uvicorn app.main:app --reload --port 8000`
  - Frontend: `cd frontend && npm install && npm run dev` — Vite corre en `:5173` y su proxy (`vite.config.js`) reenvía todo `/api/*` al backend en `:8000`, sin necesidad de configurar CORS mientras se programa.
- **Para la entrega/demo**: `cd frontend && npm run build` compila React directamente a `backend/static/` (configurado en `vite.config.js`); FastAPI detecta esa carpeta y la sirve como archivos estáticos (`StaticFiles` montado en `/`), quedando **un solo servidor y un solo puerto**: `cd backend && py -3 -m uvicorn app.main:app`. Así quien evalúe el proyecto levanta el sistema completo con un solo comando, sin instalar Node ni lidiar con CORS.
- Probado de punta a punta el 2026-09-23: health check, Swagger (`/docs`), creación del esquema SQLite y build+servido estático, los tres funcionando (ver Cambio 6 en `VALIDACION_IA.md`).
- **Despliegue**: [Render](https://render.com) (plan free), conectado a este repositorio con auto-deploy en cada push a `main`. Ya tiene configuradas estas variables de entorno (Settings → Environment):

  | Variable | Para qué sirve |
  |---|---|
  | `JWT_SECRET_KEY` | Firma los JWT de clientes y administrador. |
  | `ADMIN_EMAIL` / `ADMIN_PASSWORD` | Credenciales del único administrador del sistema (§ Roles y autorización). |

  Si alguna de las tres falta, `backend/app/seguridad.py` genera un valor aleatorio solo para esa ejecución (nunca un literal fijo en el código — ver Cambio 18 en `VALIDACION_IA.md`), así que en local funciona sin configurar nada, pero en Render conviene tenerlas fijas para que las sesiones no se invaliden en cada reinicio del servicio.

## 7. Plan de trabajo

Desarrollo individual. El sistema se aborda en **franjas verticales por dominio** (cada una cubre su modelo, su parte de la API y su pantalla en React) en vez de por capa (todo el backend primero, todo el frontend después), para ir entregando funcionalidad completa y demostrable dominio por dominio. Cada franja agrupa las reglas de negocio (R1-R17) que le corresponden:

| Dominio | Reglas | Incluye |
|---|---|---|
| **Destinos** | R1, R2, R8 | Modelo y CRUD de destinos, alta/baja lógica (no disponible), listado del catálogo (backend + pantalla React) |
| **Paquetes** | R3, R4, R5, R6, R7 | Armado de paquetes combinando destinos, cálculo de precio con margen, fijación del precio al publicar, catálogo público de paquetes (backend + pantalla React) |
| **Clientes y seguridad** | R9, R10, R11, R17 | Registro, login, hash de contraseñas, JWT, protección de RUT/teléfono en listados y errores (backend + pantallas de registro/login) |
| **Reservas** | R12, R13, R14, R15, R16 | Reservar un paquete, cálculo del total, control de cupo y de fecha vencida, historial propio del cliente (backend + pantalla de reservas) |

**Trabajo ya realizado:** esqueleto de `backend/` (FastAPI + esquema SQLite) y `frontend/` (React + Vite), con las 5 tablas ya creadas:

| Tabla | Contenido |
|---|---|
| `destinos` | R1, R2, R8 (nombre único, costo > 0, `disponible`) |
| `paquetes` | R5, R6, R7 (fechas, cupo, margen, `precio_publicado`, `publicado`) |
| `paquete_destinos` | relación N:N entre paquetes y destinos (R3, R4) |
| `clientes` | R9 (correo único), R10 (`password_hash`) |
| `reservas` | R12, R13, R16 (cliente, paquete, personas, total) |

Las reglas que no se expresan como restricción de columna (R3 combinación 2-5 destinos sin repetir, R4, R14 cupo disponible, R15 fecha vencida) quedan para la lógica de cada dominio en su router, no en el esquema.

**Flujo de trabajo:** dado el plazo de entrega (5 de octubre), se commitea y pushea directo a `main` (sin Pull Request, al ser desarrollo individual). Cada cambio de código sigue actualizando `README.md` + `VALIDACION_IA.md` (ver [§9](#9-uso-de-ia-y-registro-de-cambios)) para mantener la trazabilidad exigida por la rúbrica.

## 8. Estado actual y próximos pasos

Los 4 dominios del plan de trabajo (§7) están implementados y probados de punta a punta: Destinos (R1, R2, R8), Paquetes (R3-R7), Clientes y seguridad (R9, R10, R11, R17) y Reservas (R12-R16) — con autenticación JWT, hash de contraseñas con `bcrypt`, rol de administrador separado del de cliente, 43 pruebas automatizadas (`backend/tests/`), modelo UML ([`docs/modelo-uml.md`](docs/modelo-uml.md)) y SonarCloud sin hallazgos abiertos (Quality Gate en `OK`). Las variables `JWT_SECRET_KEY`/`ADMIN_EMAIL`/`ADMIN_PASSWORD` ya están configuradas en Render (ver §6). Pendiente, si el tiempo alcanza: más pruebas de integración end-to-end desde el frontend y ajustar la estructura de este documento cuando se conozca la guía oficial de evaluación.

## 9. Uso de IA y registro de cambios

Cada cambio de código de este proyecto se documenta en `VALIDACION_IA.md` (objetivo, implementación, revisión técnica y validación), siguiendo el mismo estándar que EcoTechSolutions.
