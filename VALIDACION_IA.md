# Validación de cambios apoyados por IA

Registro técnico del proyecto Viajes Aventura (TI3V21, INACAP). Documenta cada cambio relevante del código con la misma estructura: **objetivo**, **implementación**, **revisión técnica** (qué propuso la IA o qué alternativa se evaluó, y por qué se adoptó, modificó o descartó) y **validación** (pruebas ejecutadas y su resultado). Los cambios se numeran en orden cronológico.

## Índice

- [Cambio 1 - Documentación inicial del proyecto](#cambio-1---documentación-inicial-del-proyecto)
- [Cambio 2 - Definición de arquitectura: backend Python (FastAPI) + frontend React](#cambio-2---definición-de-arquitectura-backend-python-fastapi--frontend-react)
- [Cambio 3 - Plan de trabajo por dominio](#cambio-3---plan-de-trabajo-por-dominio)
- [Cambio 4 - Servidor único: FastAPI sirve el frontend compilado](#cambio-4---servidor-único-fastapi-sirve-el-frontend-compilado)
- [Cambio 5 - Esqueleto base: backend FastAPI, frontend React y esquema SQLite](#cambio-5---esqueleto-base-backend-fastapi-frontend-react-y-esquema-sqlite)
- [Cambio 6 - Dominio Destinos: CRUD y catálogo (R1, R2, R8)](#cambio-6---dominio-destinos-crud-y-catálogo-r1-r2-r8)
- [Cambio 7 - Dominio Paquetes: armado, precio y publicación (R3-R7)](#cambio-7---dominio-paquetes-armado-precio-y-publicación-r3-r7)
- [Cambio 8 - Dominio Clientes y seguridad: registro, login y JWT (R9, R10, R11, R17)](#cambio-8---dominio-clientes-y-seguridad-registro-login-y-jwt-r9-r10-r11-r17)

### Cambio 1 - Documentación inicial del proyecto

**Fecha:** 2026-09-23
**Archivos creados:** `README.md`, `VALIDACION_IA.md`
**Objetivo:** dejar registrado el caso de estudio y establecer, antes de escribir código, la bitácora de trazabilidad para cada cambio posterior.

#### Implementación

Se leyó `Viajes_aventura.pdf` (antecedentes de la Unidad 4, caso "Agencia de Viajes") y se redactó `README.md` con el resumen del negocio, el problema actual de la agencia, las 17 reglas de negocio confirmadas (R1-R17), el alcance dentro/fuera acordado por los socios y los vacíos del caso que exigen un supuesto explícito. Se recomendó Python 3 + SQLite como stack, por consistencia con el proyecto EcoTechSolutions del mismo autor y la misma asignatura, y se creó este archivo para iniciar el registro de cambios.

#### Revisión técnica

El resumen del caso se contrastó frase por frase contra el PDF para no omitir ninguna regla de negocio (R1-R17) ni los límites de alcance declarados en la sección 6 del documento. Se evitó traducir las reglas de negocio en requerimientos de sistema dentro del README, ya que el propio caso indica que esa traducción es parte del trabajo evaluado y no un dato entregado.

#### Validación

Se verificó que las 17 reglas y las tablas de alcance (dentro/fuera) del README coincidan con el texto del PDF sin omisiones ni reinterpretaciones. Pendiente: iniciar repositorio git para este proyecto (aún no versionado) antes del próximo cambio de código.

### Cambio 2 - Definición de arquitectura: backend Python (FastAPI) + frontend React

**Fecha:** 2026-09-23
**Archivo modificado:** `README.md`
**Objetivo:** registrar la decisión de separar el sistema en backend Python y frontend React, indicada por el usuario, y elegir un framework concreto para el backend.

#### Implementación

Se actualizó el README: la tabla de tecnología pasó de "Python + SQLite" (aplicación de consola, como EcoTechSolutions) a una arquitectura de dos partes — `backend/` (API REST/JSON) y `frontend/` (cliente React que solo habla HTTP con el backend, sin acceso directo a la base de datos). Se añadió la sección 6 con el detalle de cada carpeta y se ajustó la sección 7 (próximos pasos) para reflejar la nueva estructura.

#### Revisión técnica

El usuario definió los lenguajes (React / Python) pero no el framework de backend. Se evaluaron Flask y FastAPI; se propuso **FastAPI** por tres razones verificables contra las reglas de negocio: (1) valida tipos y rangos de entrada con Pydantic, relevante para R2, R5, R6 y R16; (2) genera documentación interactiva (`/docs`) para probar la API antes de tener frontend; (3) su modelo async es apropiado para un backend consumido por un cliente separado. La elección se presentó como recomendación, no como decisión unilateral, dejando abierto el cambio de framework si el usuario lo prefiere.

#### Validación

No aplica ejecución de código en este cambio (solo documentación). Queda pendiente crear la estructura real de carpetas `backend/` y `frontend/` en el próximo cambio.

### Cambio 3 - Plan de trabajo por dominio

**Fecha:** 2026-09-23
**Archivo modificado:** `README.md`
**Objetivo:** organizar el desarrollo en franjas por dominio antes de escribir código, para avanzar de forma ordenada y entregar funcionalidad completa dominio por dominio.

#### Implementación

Se agregó la sección "Plan de trabajo" al README, dividiendo el sistema en 4 franjas verticales por dominio (cada una con su modelo, su parte de la API FastAPI y su pantalla React), en vez de dividir por capa: **Destinos** (R1, R2, R8), **Paquetes** (R3-R7), **Clientes y seguridad** (R9, R10, R11, R17) y **Reservas** (R12-R16). Se documentó también el trabajo ya realizado (esqueleto de `backend/`/`frontend/` y esquema SQLite) y el flujo de trabajo (commit y push directo a `main`).

#### Revisión técnica

Se evaluó dividir por capa (todo el backend primero, todo el frontend después) frente a dividir por dominio vertical; se adoptó la segunda porque el caso ya separa sus reglas de negocio en grupos temáticos claros (destinos / paquetes / clientes / reservas), lo que permite entregar cada vez una funcionalidad completa y demostrable de principio a fin.

#### Validación

No aplica ejecución de código en este cambio (solo documentación). Pendiente: crear el esqueleto de `backend/`/`frontend/` y el esquema SQLite antes de comenzar el primer dominio.

### Cambio 4 - Servidor único: FastAPI sirve el frontend compilado

**Fecha:** 2026-09-23
**Archivo modificado:** `README.md`
**Objetivo:** simplificar la entrega y demostración del sistema (fecha límite 5 de octubre) para que se ejecute con un solo comando, sin dejar de tener backend y frontend como códigos separados.

#### Implementación

Se agregó al README, dentro de la sección 6, la explicación de dos modos de ejecución: desarrollo con dos procesos separados (`uvicorn` + `npm start` con proxy, para mantener la recarga en caliente de React) y entrega/demo con un solo proceso, donde FastAPI sirve el build estático de React (`StaticFiles` + ruta catch-all a `index.html`) desde el mismo puerto que la API.

#### Revisión técnica

El usuario preguntó si se podía trabajar "full stack" en vez de "separado"; se aclaró que se refería a evitar dos servidores corriendo por separado para la entrega, no a fusionar el trabajo por dominio (eso no cambia). Se evaluó mantener siempre dos servidores frente a servir el build de React desde FastAPI solo para la demo; se adoptó la segunda por ser el patrón estándar para este tipo de proyecto académico: evita configurar CORS y evita que quien evalúe tenga que instalar Node.

#### Validación

No aplica ejecución de código en este cambio (solo documentación). Pendiente: implementar el montaje de `StaticFiles` en `backend/main.py` cuando exista el esqueleto del backend.

### Cambio 5 - Esqueleto base: backend FastAPI, frontend React y esquema SQLite

**Fecha:** 2026-09-23
**Archivos creados:** `backend/app/main.py`, `backend/app/database.py`, `backend/app/__init__.py`, `backend/requirements.txt`, `frontend/` (proyecto Vite + React completo), `.gitignore`
**Objetivo:** construir la base sobre la que se desarrolla cada dominio (§7), sin reconstruirla desde cero al empezar cada uno.

#### Implementación

Backend: se creó el paquete `backend/app/` con `database.py` (conexión SQLite con `PRAGMA foreign_keys = ON` y el esquema de las 5 tablas — `destinos`, `paquetes`, `paquete_destinos`, `clientes`, `reservas` — con las restricciones `CHECK`/`UNIQUE`/`NOT NULL` derivadas de R1, R2, R5, R6, R7, R8, R9, R12, R13 y R16) y `main.py` (app FastAPI con `lifespan` que inicializa la base al arrancar, endpoint `/api/health`, y montaje condicional de `backend/static/` vía `StaticFiles` para servir el build de React). Se agregó `requirements.txt` con FastAPI, Uvicorn, Pydantic, Passlib+bcrypt, PyJWT y python-multipart (estas tres últimas para cuando se implemente el dominio de Clientes y seguridad).

Frontend: se generó el proyecto con `npm create vite@latest frontend -- --template react`, se configuró `vite.config.js` con proxy de `/api` hacia `http://localhost:8000` (desarrollo) y `build.outDir` apuntando a `../backend/static` (para que el build quede donde `main.py` lo espera). Se reemplazó el `App.jsx`/`App.css` de ejemplo de Vite por una página mínima que llama a `/api/health` y muestra el resultado, como prueba de que el cableado frontend-backend funciona, y se eliminaron los assets de ejemplo (`hero.png`, `react.svg`, `vite.svg`, `icons.svg`) que ya no se usaban.

Se agregó un `.gitignore` en la raíz para no versionar `node_modules/`, el build (`backend/static/`), la base de datos (`backend/*.db`) ni entornos virtuales.

#### Revisión técnica

Se evaluó usar Create React App frente a Vite para el frontend; se eligió Vite por ser el estándar actual (CRA está deprecado), build mucho más rápido y configuración de proxy/outDir más simple para el patrón de servidor único ya decidido en el Cambio 4. Para el manejo de errores y transacciones de `sqlite3` no se agregó código adicional en este cambio porque cada dominio lo necesita de forma distinta (por ejemplo, `paquetes` necesita transacción para la tabla puente `paquete_destinos`); agregarlo aquí habría sido una implementación a medias sin un caso de uso real todavía.

#### Validación

Se levantó el backend con `uvicorn app.main:app` y se verificó `GET /api/health` (200, `{"status":"ok"}`) y `GET /docs` (200, Swagger UI). Se confirmó por SQL directo (`sqlite_master`) que las 5 tablas se crean correctamente al iniciar la aplicación. Se corrió `npm run build` en `frontend/` y se verificó que el resultado se genera en `backend/static/`. Se volvió a levantar el backend con ese build ya presente y se confirmó que `GET /` devuelve el `index.html` de React desde el mismo puerto que la API — validando el modo de servidor único documentado en el Cambio 4. La base de datos y el build generados durante la prueba se eliminaron antes de este commit (quedan excluidos por `.gitignore`, se generan localmente).

### Cambio 6 - Dominio Destinos: CRUD y catálogo (R1, R2, R8)

**Fecha:** 2026-09-24
**Archivos creados:** `backend/app/destinos.py`, `frontend/src/Destinos.jsx`
**Archivos modificados:** `backend/app/main.py`, `frontend/src/App.jsx`, `frontend/src/App.css`
**Objetivo:** implementar el primer dominio del plan de trabajo (§7): registrar, modificar, dejar no disponible y listar destinos del catálogo.

#### Implementación

Backend: router `destinos.py` con `GET /api/destinos` (listado, con filtro opcional `solo_disponibles`), `GET /api/destinos/{id}`, `POST /api/destinos`, `PUT /api/destinos/{id}` y `DELETE /api/destinos/{id}`. La validación de tipos y rangos (nombre no vacío, `duracion_dias > 0`, `costo_base > 0` — R1, R2) queda a cargo de Pydantic (`Field(gt=0)`, `min_length=1`). La unicidad del nombre (R1) se resuelve dejando que la `UNIQUE` de la tabla falle y capturando `sqlite3.IntegrityError` para devolver 409, en vez de hacer un `SELECT` previo (evita una condición de carrera entre el chequeo y el insert). El borrado (R8) primero revisa si el destino aparece en `paquete_destinos`: si no aparece, se hace `DELETE` real; si aparece, se marca `disponible = 0` en vez de borrarlo, conservando su contenido en los paquetes ya armados. Se registró el router en `main.py`.

Frontend: componente `Destinos.jsx` con formulario de alta y tabla del catálogo (nombre, zona, duración, costo base, estado disponible/no disponible, botón eliminar), consumiendo los mismos endpoints. `App.jsx` se simplificó para renderizar este componente en vez del health-check de prueba.

#### Revisión técnica

Se evaluó validar la unicidad del nombre con un `SELECT` previo al `INSERT` frente a capturar la excepción de la restricción `UNIQUE` existente en el esquema; se adoptó la segunda porque el esquema ya la declara (Cambio 5) y evita una consulta extra además de la condición de carrera propia del patrón check-then-act. Para R8 se evaluó pedir al cliente que indique si quiere "eliminar" o "deshabilitar" frente a que el propio backend decida según si el destino está en uso; se adoptó la segunda porque la regla de negocio ya define el criterio de forma determinista y no admite ambigüedad ni deja la decisión en manos del cliente HTTP.

#### Validación

Probado con el backend corriendo localmente (`uvicorn`, puertos 8001/8002 para no chocar con otras pruebas): creación (201) y verificación de los datos devueltos; creación duplicada del mismo nombre (409); costo base 0 rechazado por Pydantic (422); eliminación de un destino sin paquetes asociados (se borra, el listado posterior queda vacío); eliminación de un destino insertado manualmente en `paquete_destinos` (queda `disponible: false` y sigue apareciendo en el listado, no se borra). Se corrió `npm run build` en `frontend/` y compiló sin errores (18 módulos). La base de datos y el build generados durante las pruebas se eliminaron antes de este commit (excluidos por `.gitignore`).

### Cambio 7 - Dominio Paquetes: armado, precio y publicación (R3-R7)

**Fecha:** 2026-09-24
**Archivos creados:** `backend/app/paquetes.py`, `frontend/src/Paquetes.jsx`
**Archivos modificados:** `backend/app/main.py`, `frontend/src/App.jsx`, `frontend/src/App.css`
**Objetivo:** implementar el segundo dominio del plan de trabajo (§7): armar paquetes combinando destinos, calcular el precio con margen y consultar disponibilidad.

#### Implementación

Backend: router `paquetes.py` con `GET /api/paquetes`, `GET /api/paquetes/{id}`, `POST /api/paquetes` y `POST /api/paquetes/{id}/publicar` (sin `PUT`/`DELETE`: la sección 4 del README solo pide crear, calcular precio y consultar disponibilidad para este dominio, no modificar). El esquema `PaqueteCreate` valida con Pydantic: `cupo_maximo > 0` (R5), `destino_ids` con `min_length=2, max_length=5` y sin duplicados vía `field_validator` (R3), y `fecha_regreso` posterior a `fecha_salida` vía otro `field_validator` que compara contra el campo ya validado (R5). Antes de insertar, `_validar_destinos_disponibles` confirma que todos los `destino_ids` existan y tengan `disponible = 1` (cruce con R8: un destino no disponible no puede usarse en paquetes nuevos). La creación de `paquetes` + sus filas en `paquete_destinos` corre en una única transacción (rollback si falla el `INSERT` en `paquete_destinos`). El precio (R6) se calcula como `round(suma_costo_base * (1 + margen))`; mientras el paquete no está publicado se recalcula al vuelo desde los costos actuales de sus destinos, y `POST /publicar` lo calcula una vez y lo guarda en `precio_publicado` con `publicado = 1` (R7), devolviendo 409 si ya estaba publicado. `cupo_disponible` se calcula como `cupo_maximo - SUM(personas)` desde `reservas` (tabla vacía por ahora, queda listo para el dominio Reservas).

Frontend: componente `Paquetes.jsx` con formulario (nombre, fechas, cupo, margen, checklist de destinos disponibles obtenidos de `GET /api/destinos?solo_disponibles=true`) y tabla de paquetes (fechas, destinos incluidos, cupo disponible, precio, estado publicado/borrador y botón "Publicar" para los no publicados).

#### Revisión técnica

Se evaluó fijar el precio ya en la creación del paquete frente a calcularlo al vuelo hasta la publicación; se adoptó la segunda porque R7 dice explícitamente que el precio "queda fijado cuando el paquete se publica", lo que implica que antes de eso debe reflejar los costos vigentes (por ejemplo, si se corrige el costo base de un destino antes de publicar el paquete, el precio del borrador debe verse afectado; una vez publicado, no). Se evaluó devolver error o auto-excluir destinos no disponibles al armar un paquete nuevo; se adoptó devolver 409 con el detalle de qué IDs no están disponibles, siguiendo el mismo criterio explícito-antes-que-implícito usado en el resto del proyecto, en vez de silenciar la exclusión. No se implementó `PUT`/`DELETE` de paquetes por no estar dentro del alcance declarado en el README para este dominio; si se requiere corregir un paquete no publicado, queda como vacío del caso a resolver más adelante (documentado, no implementado a medias).

#### Validación

Backend probado localmente con `uvicorn` (puerto 8003): creación de un paquete con 2 destinos (100.000 + 50.000, margen 0.20) devuelve precio 180.000; publicar el paquete fija `publicado: true` y `precio: 180.000`; publicar de nuevo devuelve 409; se cambió el costo base de uno de sus destinos a 999.999 y el precio publicado siguió en 180.000 (R7 verificado); crear un paquete con un solo destino (422, R3), con un destino repetido (422, R3), con más de 5 destinos (422, R3), con fecha de regreso anterior a la de salida (422, R5) y usando un destino marcado `disponible = 0` (409, cruce con R8) — todos los casos se comportaron como se esperaba. Se corrió `npm run build` en `frontend/` y compiló sin errores (19 módulos). La base de datos generada durante las pruebas se eliminó antes de este commit (excluida por `.gitignore`).

### Cambio 8 - Dominio Clientes y seguridad: registro, login y JWT (R9, R10, R11, R17)

**Fecha:** 2026-09-24
**Archivos creados:** `backend/app/clientes.py`, `backend/app/seguridad.py`, `frontend/src/Clientes.jsx`
**Archivos modificados:** `backend/app/main.py`, `backend/requirements.txt`, `frontend/src/App.jsx`, `frontend/src/App.css`
**Objetivo:** implementar el tercer dominio del plan de trabajo (§7): registro y autenticación de clientes, protegiendo credenciales y datos sensibles.

#### Implementación

Backend: `seguridad.py` concentra el hash de contraseñas y el manejo de JWT (independiente del router para poder reutilizarlo desde el dominio Reservas más adelante). `clientes.py` expone `POST /api/clientes/registro`, `POST /api/clientes/login` y `GET /api/clientes/me` (protegido). El esquema `ClienteRegistro` valida con Pydantic: `nombre`/`telefono` no vacíos, `correo` con `EmailStr`, `password` entre 8 y 72 caracteres (R9), y un `field_validator` propio (`_rut_valido`) que calcula el dígito verificador del RUT chileno con el algoritmo módulo 11 y rechaza formatos o dígitos inválidos. La unicidad del correo (R9) se resuelve capturando `sqlite3.IntegrityError` sobre la `UNIQUE` de la tabla, igual que en Destinos. La contraseña se hashea con `bcrypt.hashpw`/`gensalt` antes de guardarla y nunca se compara ni se registra en texto plano (R10). `POST /login` devuelve el mismo error genérico ("Correo o contraseña incorrectos") tanto si el correo no existe como si la contraseña es incorrecta, para no revelar qué correos están registrados. `obtener_cliente_actual` es una dependencia de FastAPI (`HTTPBearer`) que decodifica el JWT, verifica que el cliente siga existiendo y devuelve su id; `GET /me` la usa para exponer solo el perfil del propio cliente autenticado (R11). El modelo de respuesta `ClientePerfil` (`id`, `nombre`, `correo`) nunca incluye `rut` ni `telefono` en ninguna respuesta de la API —ni siquiera en el propio perfil— como cumplimiento estricto de R17.

Frontend: componente `Clientes.jsx` con pestañas "Iniciar sesión"/"Registrarme", que guarda el JWT recibido en `localStorage` y, si hay sesión activa, llama a `GET /api/clientes/me` para mostrar el nombre y correo del cliente junto con un botón "Cerrar sesión".

#### Revisión técnica

Se evaluó usar `passlib[bcrypt]` (ya estaba en `requirements.txt` desde el Cambio 6) frente a usar la librería `bcrypt` directamente; al probar el registro, `passlib` 1.7.4 falló con `AttributeError: module 'bcrypt' has no attribute '__about__'` y luego con `ValueError: password cannot be longer than 72 bytes` durante su propio auto-test interno de compatibilidad — un bug conocido de `passlib` (sin mantención desde 2020) contra versiones de `bcrypt` >= 4.1. Se optó por quitar `passlib` y hashear directamente con `bcrypt.hashpw`/`bcrypt.checkpw`, más simple y sin la capa de compatibilidad rota; se dejó `max_length=72` en el campo `password` porque ese es un límite propio del algoritmo bcrypt, no arbitrario. Se evaluó no restringir R17 solo a "listados" (como dice literalmente la regla) y permitir que el propio cliente vea su RUT/teléfono en `/me`, frente a no exponerlos nunca vía API; se adoptó la segunda por ser la interpretación más estricta y simple de sostener (ninguna respuesta necesita filtrar campos según quién pregunta), documentado aquí como supuesto explícito. Se evaluó devolver un error distinto para "correo no existe" vs. "contraseña incorrecta" en el login frente a un mensaje genérico único; se adoptó el mensaje único porque distinguir esos casos permite enumerar correos registrados probando contraseñas al azar.

#### Validación

Backend probado localmente con `uvicorn`: registro con un RUT válido (`12345678-5`, verificado por cálculo manual del dígito verificador) devuelve 201 con `access_token` y un `cliente` sin `rut` ni `telefono`; registro repitiendo el mismo correo (409); RUT con dígito verificador incorrecto (422); contraseña de 3 caracteres (422); login con la contraseña correcta devuelve un token nuevo; login con contraseña incorrecta (401); `GET /me` con el token devuelve el perfil correcto; `GET /me` sin header `Authorization` (401) y con un token inventado (401). Se corrió `npm run build` en `frontend/` y compiló sin errores (20 módulos). La base de datos generada durante las pruebas se eliminó antes de este commit (excluida por `.gitignore`).
