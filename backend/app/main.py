from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Viajes Aventura API", lifespan=lifespan)


@app.get("/api/health")
def health():
    return {"status": "ok"}


# Cada dominio (destinos, paquetes, clientes, reservas) agrega su router aqui
# con app.include_router(...) a medida que se implementa.

STATIC_DIR = Path(__file__).parent.parent / "static"
if STATIC_DIR.exists():
    # Build de React (npm run build en frontend/), servido en el mismo puerto que la API.
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
