from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import crear_tablas, sembrar_datos
from routers import auth, categorias, pedidos, productos, usuarios


@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas()
    sembrar_datos()
    yield


app = FastAPI(
    title="API Tienda Persistente",
    description="API REST con FastAPI, JWT, roles y persistencia en SQLite3.",
    version="0.5.0",
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(categorias.router)
app.include_router(usuarios.router)
app.include_router(pedidos.router)


@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "API Tienda Persistente funcionando correctamente"}
