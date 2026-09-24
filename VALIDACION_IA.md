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
- [Cambio 9 - Dominio Reservas: reservar, cupo y fecha vencida (R12-R16)](#cambio-9---dominio-reservas-reservar-cupo-y-fecha-vencida-r12-r16)
- [Cambio 10 - Rol de administrador separado del de cliente](#cambio-10---rol-de-administrador-separado-del-de-cliente)
- [Cambio 11 - Suite de pruebas automatizadas (pytest)](#cambio-11---suite-de-pruebas-automatizadas-pytest)
- [Cambio 12 - Modelo UML del dominio](#cambio-12---modelo-uml-del-dominio)
- [Cambio 13 - Rediseño visual del frontend](#cambio-13---rediseño-visual-del-frontend)
- [Cambio 14 - Auditoría contra el PDF del caso: tabla de supuestos explícitos](#cambio-14---auditoría-contra-el-pdf-del-caso-tabla-de-supuestos-explícitos)
- [Cambio 15 - Condición de carrera en el cupo de Reservas (R14)](#cambio-15---condición-de-carrera-en-el-cupo-de-reservas-r14)

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

### Cambio 9 - Dominio Reservas: reservar, cupo y fecha vencida (R12-R16)

**Fecha:** 2026-09-24
**Archivos creados:** `backend/app/reservas.py`, `frontend/src/Reservas.jsx`
**Archivos modificados:** `backend/app/main.py`, `frontend/src/App.jsx`, `frontend/src/Clientes.jsx`
**Objetivo:** implementar el cuarto y último dominio del plan de trabajo (§7): reservar un paquete, calcular el total, controlar cupo y fecha vencida, y consultar el historial propio.

#### Implementación

Backend: router `reservas.py` con `GET /api/reservas` (historial propio) y `POST /api/reservas` (crear reserva), ambos protegidos con la dependencia `obtener_cliente_actual` del Cambio 8 — el `cliente_id` sale del JWT, nunca del cuerpo de la petición, así que un cliente no puede reservar ni consultar a nombre de otro (R11). `POST /api/reservas` valida en orden: el paquete existe (404); está publicado (409 — ver supuesto abajo); su `fecha_salida` no es anterior a hoy (409, R15); el cupo disponible (`cupo_maximo - SUM(personas)` de las reservas existentes) alcanza para la cantidad pedida (409, R14); y `personas >= 1` vía `Field(ge=1)` de Pydantic (422, R16). El `total` se calcula como `precio_publicado * personas` en el momento de crear la fila y quedar grabado en la tabla `reservas` (R13) — no se vuelve a tocar aunque cambie después el margen o el costo de un destino. `GET /api/reservas` filtra por `cliente_id` (R11) y devuelve cada reserva con un resumen del paquete asociado (nombre y fechas) mediante un `JOIN`.

Frontend: se subió el estado de sesión (`token`, `perfil`) desde `Clientes.jsx` hasta `App.jsx`, que ahora hace el `fetch` a `/api/clientes/me` y pasa `perfil`/`onSesionIniciada`/`onCerrarSesion` como props — necesario para que el nuevo componente `Reservas.jsx` (hermano de `Clientes`) sepa si hay sesión activa sin duplicar el estado de login. `Reservas.jsx` muestra un selector con los paquetes publicados (nombre, precio, cupo disponible) y un formulario para reservar, además de una tabla con el historial propio (`GET /api/reservas`); si no hay sesión iniciada, solo invita a iniciar sesión.

#### Revisión técnica

Se evaluó permitir reservar paquetes no publicados (usando el precio calculado al vuelo) frente a exigir que estén publicados; se adoptó la segunda como supuesto explícito, documentado también en el código: un paquete sin publicar es un borrador que el administrador todavía puede estar ajustando, y R7 solo garantiza estabilidad de precio a partir de la publicación, así que permitir reservarlo antes introduciría el mismo problema que la planilla actual (cambiar de precio algo ya "vendido"). Se evaluó levantar el estado de sesión a un contexto de React (`useContext`) frente a subirlo al componente padre común (`App.jsx`) y pasarlo por props; con solo dos componentes consumidores (`Clientes` y `Reservas`) y una jerarquía de un solo nivel, pasar props es más simple y suficiente — un Context solo se justificaría si creciera la profundidad de componentes.

#### Validación

Backend probado localmente con `uvicorn`: reservar un paquete recién creado sin publicar (409); tras publicarlo (precio 180.000), reservar 2 personas devuelve total 360.000 (R13 verificado); con cupo máximo 3 y 2 ya reservadas, pedir 2 más devuelve 409 con el cupo restante en el mensaje (R14); reservar exactamente el cupo restante (1) devuelve 201; `personas: 0` devuelve 422 (R16); reservar un paquete publicado con `fecha_salida` en el pasado devuelve 409 (R15); `POST /api/reservas` sin header `Authorization` devuelve 401; se registró un segundo cliente y su `GET /api/reservas` devolvió `[]` a pesar de existir reservas de otro cliente (R11 verificado). Se corrió `npm run build` en `frontend/` y compiló sin errores (21 módulos). La base de datos generada durante las pruebas se eliminó antes de este commit (excluida por `.gitignore`).

Con este cambio quedan implementados los cuatro dominios del plan de trabajo (§7) y las 17 reglas de negocio (R1-R17).

### Cambio 10 - Rol de administrador separado del de cliente

**Fecha:** 2026-09-24
**Archivos creados:** `backend/app/admin.py`, `frontend/src/Admin.jsx`
**Archivos modificados:** `backend/app/seguridad.py`, `backend/app/clientes.py`, `backend/app/destinos.py`, `backend/app/paquetes.py`, `backend/app/main.py`, `frontend/src/App.jsx`, `frontend/src/Destinos.jsx`, `frontend/src/Paquetes.jsx`, `README.md`
**Objetivo:** cerrar una brecha de seguridad detectada al revisar el proyecto ya completo: los endpoints de administración (crear/editar/eliminar destinos, crear/publicar paquetes) no tenían ninguna autenticación — cualquiera con la URL podía modificar el catálogo. El caso describe explícitamente un rol "Administrador" separado del cliente (`Viajes_aventura.pdf` §1.3), que hasta este cambio no estaba modelado.

#### Implementación

`seguridad.py`: el JWT ahora incluye un claim `rol` (`"cliente"` o `"admin"`) además de `sub`; `crear_token(sujeto, rol)` lo recibe explícito. `obtener_cliente_actual` ahora exige `rol == "cliente"` (antes solo validaba que el `sub` fuera un id de cliente existente) y se agrega `obtener_admin_actual`, que exige `rol == "admin"`. Como el caso describe un único administrador (uno de los socios, no una lista de administradores), sus credenciales se leen de variables de entorno (`ADMIN_EMAIL`, `ADMIN_PASSWORD`) en vez de una tabla nueva; `verificar_credenciales_admin` las compara con `secrets.compare_digest` (comparación a tiempo constante, evita timing attacks). `admin.py` agrega `POST /api/admin/login`. Se protegieron con `Depends(obtener_admin_actual)`: `POST/PUT/DELETE /api/destinos` y `POST /api/paquetes` + `POST /api/paquetes/{id}/publicar`; los `GET` (catálogo) siguen públicos, ya que el caso los describe como consulta abierta para clientes.

Frontend: nuevo componente `Admin.jsx` con login de administrador (token guardado en `localStorage` bajo una clave separada de la del cliente). El estado `adminToken` se subió a `App.jsx` y se pasa como prop a `Destinos.jsx` y `Paquetes.jsx`, que ahora envían el header `Authorization` en sus llamadas de escritura y ocultan los formularios de creación/botones de eliminar/publicar cuando no hay sesión de administrador activa.

#### Revisión técnica

Se evaluó agregar un campo `es_admin` en la tabla `clientes` (reutilizando el modelo de autenticación ya existente) frente a un administrador único fuera de la base de datos; se adoptó la segunda porque el caso es explícito en que hay un solo administrador (un socio), no una lista abierta de cuentas con privilegios variables — modelar una tabla completa de roles habría sido una implementación a medias sin un caso de uso real (no hay forma en el caso de que se registre un segundo administrador). Se documenta como riesgo conocido: las credenciales de administrador de desarrollo quedan visibles en el código fuente (repositorio público), así que es obligatorio configurar `ADMIN_EMAIL`/`ADMIN_PASSWORD`/`JWT_SECRET_KEY` como variables de entorno reales en Render antes de considerar el despliegue seguro (ver README §6); esto no se pudo hacer desde este entorno por no contar con acceso al dashboard de Render.

#### Validación

Backend probado localmente con `uvicorn`: crear un destino sin token (401); login de administrador con credenciales incorrectas (401) y correctas (200, devuelve token); crear un destino con el token de administrador (201); crear un destino con un token de **cliente** válido (403, rol incorrecto); `GET /api/clientes/me` con un token de **administrador** (403, rol incorrecto); `GET /api/clientes/me` con un token de cliente sigue funcionando (200) — confirma que separar los roles no rompió el dominio Clientes existente. Se corrió `npm run build` en `frontend/` y compiló sin errores (22 módulos).

### Cambio 11 - Suite de pruebas automatizadas (pytest)

**Fecha:** 2026-09-24
**Archivos creados:** `backend/pytest.ini`, `backend/requirements-dev.txt`, `backend/tests/conftest.py`, `backend/tests/test_destinos.py`, `backend/tests/test_paquetes.py`, `backend/tests/test_clientes.py`, `backend/tests/test_reservas.py`, `backend/tests/test_admin.py`
**Objetivo:** cubrir con pruebas automatizadas las 17 reglas de negocio y la separación de roles del Cambio 10, en vez de depender solo de pruebas manuales con `curl` (como en los Cambios 6-10).

#### Implementación

`conftest.py` define el fixture `client`, que monkeypatchea `app.database.DB_PATH` a un archivo SQLite temporal por test (vía `tmp_path` de pytest) y crea un `TestClient` de FastAPI dentro de un `with` (para disparar el `lifespan` y correr `init_db()`), logrando aislamiento total entre pruebas sin tocar la base de datos real del proyecto. Las variables `JWT_SECRET_KEY`/`ADMIN_EMAIL`/`ADMIN_PASSWORD` se fijan con `os.environ.setdefault(...)` **antes** de importar `app.main`, porque `seguridad.py` las lee como constantes de módulo al importarse. Se agregaron funciones de apoyo (`crear_destino`, `crear_paquete`, `registrar_cliente`, `cliente_headers`) reutilizadas entre los 5 archivos de test. `backend/requirements-dev.txt` agrega `pytest` y `httpx` sobre `requirements.txt`, en un archivo separado para no instalar dependencias de testing en el build de producción de Render. `backend/pytest.ini` fija `pythonpath = .` para que `from app...` resuelva al correr `pytest` desde `backend/`.

Cobertura por dominio: **Destinos** (R1 nombre único, R2 costo > 0, R8 borrado vs. baja lógica, escritura requiere admin); **Paquetes** (R3 mínimo/máximo/sin repetidos, R5 fechas/cupo, R6 cálculo de precio, R7 precio fijo tras publicar y no se puede publicar dos veces, cruce con R8, escritura requiere admin); **Clientes** (R9 correo único y RUT inválido, R10 password hasheada — se verifica leyendo `password_hash` directo de la base de prueba y comparando contra el texto plano —, R17 `rut`/`telefono` nunca presentes en ninguna respuesta); **Reservas** (R11 aislamiento entre clientes y autenticación requerida, R12/R13 total fijado, R14 cupo, R15 fecha vencida, R16 personas ≥ 1, paquete debe estar publicado); **Admin** (login correcto/incorrecto, un token de cliente no sirve de administrador y viceversa).

#### Revisión técnica

Se evaluó una base de datos SQLite en memoria (`:memory:`) compartida entre tests frente a un archivo temporal por test; se adoptó el archivo temporal porque cada conexión nueva a `:memory:` en `sqlite3` crea una base distinta (no hay una sola base en memoria compartida entre conexiones sin configuración adicional como URI mode), y el código de la aplicación abre una conexión nueva por request (`get_connection()` en cada función) — un archivo temporal real evita ese problema sin tener que tocar el código de producción para las pruebas. Se evaluó un archivo `requirements.txt` único con `pytest` incluido frente a separar `requirements-dev.txt`; se adoptó la segunda para que el build de Render (que instala `requirements.txt`) no cargue dependencias de testing en producción.

#### Validación

`cd backend && py -3 -m pytest` — **37 pruebas, todas pasan**, en aproximadamente 4 segundos. Sin advertencias tras ajustar la clave JWT de prueba a 32+ bytes (la de desarrollo original de 16 bytes generaba un `InsecureKeyLengthWarning` de `pyjwt`).

### Cambio 12 - Modelo UML del dominio

**Fecha:** 2026-09-24
**Archivo creado:** `docs/modelo-uml.md`
**Archivo modificado:** `README.md`
**Objetivo:** dejar un modelo UML formal del dominio (destinos, paquetes, clientes, reservas), pendiente desde el Cambio 9.

#### Implementación

Diagrama de clases en sintaxis Mermaid (se renderiza directo en GitHub, sin herramientas externas): `Destino`, `Paquete`, `Cliente`, `Reserva` con sus atributos derivados del esquema SQL (`backend/app/database.py`) y una clase `Administrador` marcada `<<no persistido>>` para reflejar el Cambio 10 (no es una tabla, son credenciales por variable de entorno). Las asociaciones muestran las multiplicidades de negocio: `Paquete "2..5" o-- "0..*" Destino` (R3, R4), `Cliente "1" --> "0..*" Reserva` y `Paquete "1" --> "0..*" Reserva` (R11, R12). Se agregó una tabla que mapea cada elemento del diagrama a la(s) regla(s) de negocio que representa, y una sección de notas de diseño que aclara que los métodos del diagrama (`calcularPrecio`, `publicar`, `cupoDisponible`, `verificarPassword`) son responsabilidades de negocio conceptuales — en el código actual (FastAPI + SQL directo, sin ORM) viven como funciones en los routers, no como métodos de una clase.

#### Revisión técnica

Se evaluó generar el diagrama como imagen (PNG/SVG) para incrustar en `Informe_Viajes_Aventura.docx` frente a Mermaid en Markdown; se adoptó Mermaid porque se renderiza automáticamente en GitHub (donde vive el código, la fuente de verdad) sin depender de herramientas de conversión externas, y porque el diagrama seguirá vigente a medida que el modelo cambie sin tener que regenerar una imagen a mano. Queda pendiente decidir si se incrusta también una versión renderizada en el informe Word cuando se conozca la guía oficial de evaluación (ver nota al inicio de `Informe_Viajes_Aventura.docx`).

#### Validación

Revisión manual del diagrama contra el esquema real de `backend/app/database.py` y contra las 17 reglas de negocio: cada tabla, columna relevante y relación N:N (`paquete_destinos`) tiene su contraparte en el diagrama o en la tabla de reglas. No aplica ejecución de código (solo documentación).

### Cambio 13 - Rediseño visual del frontend

**Fecha:** 2026-09-24
**Archivo modificado:** `frontend/src/App.css`
**Archivos modificados (JSX, badges y tablas envueltas):** `frontend/src/App.jsx`, `frontend/src/Destinos.jsx`, `frontend/src/Paquetes.jsx`, `frontend/src/Reservas.jsx`
**Objetivo:** el frontend usaba solo estilos HTML por defecto (sin colores, tablas sin bordes, botones nativos) desde el Cambio 6; se rediseñó visualmente sin tocar ninguna lógica de negocio.

#### Implementación

Se reescribió `App.css` con variables CSS (`:root`) para una paleta de color (teal como color primario, naranja como acento de advertencia), tarjetas (`section` con `border-radius`, sombra y borde) para cada dominio, tipografía con la pila de fuentes del sistema, formularios e inputs con estados de foco visibles, y una tabla con encabezado diferenciado y filas con hover. Se agregaron clases `.badge`/`.badge-ok`/`.badge-off`/`.badge-warn` para los estados "Disponible/No disponible" (Destinos) y "Publicado/Borrador" (Paquetes), reemplazando el texto plano. Cada tabla se envolvió en un `<div className="table-wrap">` con `overflow-x: auto` para que no rompa el layout en pantallas angostas. Se agregó un subtítulo bajo el `<h1>` en `App.jsx` y un mensaje "Todavía no hay..." cuando un catálogo está vacío (antes mostraba una tabla sin filas, sin contexto). Se agregó una media query a 520px que apila los campos del formulario a ancho completo en móvil.

#### Revisión técnica

Se evaluó una librería de componentes (p. ej. Tailwind o Material UI) frente a CSS propio con variables; se adoptó CSS propio porque el proyecto ya está en la recta final (entrega 5 de octubre) y sumar una dependencia nueva de build para un rediseño visual no aporta a las reglas de negocio evaluadas — variables CSS ya resuelven la necesidad real (consistencia de color/espaciado) sin el costo de aprendizaje ni el peso extra en el bundle.

#### Validación

Se instaló Playwright temporalmente (fuera del repo, en el directorio de trabajo de la sesión) para levantar `npm run dev` + el backend con datos de prueba (destinos y paquetes creados vía API) y tomar capturas de pantalla reales del resultado en escritorio (1280px) y en móvil (390px, iPhone 12). Ambas se revisaron visualmente: tarjetas, badges de color, tabla con encabezado y hover, tabs de "Iniciar sesión/Registrarme" con el estado activo resaltado, y el formulario apilándose correctamente en el ancho móvil sin desbordes. `console --errors` del navegador no arrojó ningún error. La base de datos de prueba y el build generado se eliminaron antes de este commit.

### Cambio 14 - Auditoría contra el PDF del caso: tabla de supuestos explícitos

**Fecha:** 2026-09-24
**Archivos modificados:** `README.md`, `Informe_Viajes_Aventura.docx`
**Objetivo:** releer `Viajes_aventura.pdf` completo y contrastarlo línea por línea contra la implementación (código + documentación) para detectar algo pendiente, a pedido del usuario.

#### Implementación

Se releyeron las 5 páginas del PDF (negocio, cómo trabajan hoy, entrevistas a los 3 socios, cifras de temporada, R1-R17 y alcance) y se verificó cada punto contra el código: las 17 reglas, los 4 dominios y el alcance dentro/fuera están cubiertos sin desviaciones (código sin cambios en este Cambio). La única brecha real encontrada fue de documentación: la sección 5 del README (`Vacíos del caso y supuestos`) solo repetía la instrucción del caso ("adopte un supuesto y fundaméntelo") sin listar los supuestos concretos ya adoptados en los Cambios 7, 8, 9 y 10 — quedaban dispersos en sus respectivas "revisión técnica" pero nunca consolidados donde el caso pide declararlos ("en el informe"). Se agregó una tabla de 7 filas (vacío del caso → supuesto adoptado → fundamento) en `README.md` §5 y la misma tabla en `Informe_Viajes_Aventura.docx` §5, cubriendo los tres vacíos que el PDF nombra explícitamente (cancelación de reservas, fin de "temporada" de un paquete, quién administra el catálogo) más cuatro adicionales detectados durante el desarrollo (paquete no publicado, edición/eliminación de paquetes, formato de RUT, catálogo público sin sesión). Se actualizaron también las secciones 6 y 8 del informe Word para reflejar el estado real del proyecto (roles, pruebas, UML, despliegue, rediseño), que habían quedado desactualizadas desde su creación en el Cambio 1 de esta bitácora (cuando solo existía el dominio Destinos).

#### Revisión técnica

Se evaluó implementar la cancelación de reservas (uno de los tres vacíos que el PDF nombra explícitamente como ejemplo) frente a solo documentar el supuesto de que queda fuera de alcance; se adoptó la segunda porque el alcance declarado en README §4 para Reservas no la incluye ("registro y autenticación de clientes, reservar un paquete, almacenar la reserva y consultar el historial propio"), y agregarla habría sido una funcionalidad no pedida por el caso ni por el usuario en esta sesión — si el profesor la exige, es una decisión de alcance a revisar con la guía oficial, no algo para adivinar ahora.

#### Validación

Verificación manual, sección por sección del PDF, contra el código y la documentación existente; no aplica ejecución de código. Se regeneró `Informe_Viajes_Aventura.docx` con el script de `docx` y se confirmó por `python-docx` que las 3 tablas del documento (reglas, vacíos y supuestos, plan de trabajo) tienen las filas y columnas esperadas.

### Cambio 15 - Condición de carrera en el cupo de Reservas (R14)

**Fecha:** 2026-09-24
**Archivos modificados:** `backend/app/reservas.py`, `backend/tests/test_reservas.py`
**Objetivo:** el usuario pidió revisar `reservas.py` en busca de mejoras. Se detectó que `crear_reserva` leía el cupo ya reservado (`SUM(personas)`) y recién después insertaba la nueva reserva, sin ningún bloqueo entre ambos pasos — dos reservas concurrentes sobre el mismo paquete podían leer el mismo cupo disponible antes de que la otra confirmara la suya, y ambas pasar la validación de R14. Es, literalmente, el mismo problema que el caso describe que sufre la agencia hoy con el cuaderno de papel (§4: "6 reservas aceptadas por sobre el cupo del paquete").

#### Implementación

Se envolvió todo el cuerpo de `crear_reserva` (desde la lectura del paquete hasta el `INSERT` de la reserva) en una transacción `BEGIN IMMEDIATE`. Para poder emitir `BEGIN IMMEDIATE` manualmente, se pone `conn.isolation_level = None` (modo autocommit) **solo en esa conexión local de la función**, sin tocar `get_connection()` en `database.py` (que sigue con el modo de transacción implícita por defecto que usan el resto de los endpoints — cambiarlo globalmente habría alterado el comportamiento de `conn.rollback()` en `paquetes.py`/`destinos.py`, que depende de ese modo). `BEGIN IMMEDIATE` toma el lock de escritura de SQLite de inmediato (no al primer `INSERT`, como hace el modo por defecto), así que una segunda transacción que intente lo mismo sobre el mismo archivo de base de datos queda bloqueada hasta que la primera haga `commit()` o `rollback()` — momento en el cual vuelve a leer el cupo ya actualizado. Se agregó `except Exception: conn.rollback(); raise` para liberar el lock también cuando se lanza un `HTTPException` (404/409) a mitad de la transacción.

#### Revisión técnica

Se evaluó una conexión SQLite global en modo autocommit (cambiar `get_connection()` en `database.py`) frente a activar el modo autocommit solo dentro de `crear_reserva`; se adoptó la segunda para minimizar el radio de impacto del cambio — el resto del código (Destinos, Paquetes, Clientes) sigue funcionando exactamente igual que antes, y el único endpoint que de verdad tiene una carrera de lectura-luego-escritura sobre un valor compartido (el cupo) es este. Se evaluó una expresión SQL atómica (`INSERT ... SELECT ... WHERE cupo >= ?`) frente a `BEGIN IMMEDIATE` + chequeo en Python; se adoptó `BEGIN IMMEDIATE` porque mantiene la lógica de negocio (mensajes de error específicos por regla: paquete no encontrado, no publicado, fecha vencida, cupo insuficiente) legible en Python en vez de comprimirla en una sola consulta SQL difícil de mantener.

#### Validación

Se agregó `test_r14_dos_reservas_concurrentes_no_sobrevenden_el_cupo`, que lanza dos reservas de 1 persona en paralelo (con `threading.Thread`) contra un paquete con `cupo_maximo=1` y espera exactamente un `201` y un `409`. Para confirmar que la prueba realmente detecta el bug (no es un test que siempre pasa), se revirtió temporalmente `reservas.py` a la versión anterior al fix (con `git show HEAD:...`) y se corrió esa prueba: falló con `[201, 201]` (las dos reservas se aceptaron, sobrevendiendo el cupo de 1). Se restauró el fix y se corrió la suite completa: **38 pruebas, todas pasan**.
