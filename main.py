from fastapi import FastAPI
from routers import categorias, productos

app = FastAPI(
    title="API Tienda",
    description="API REST modularizada para una tienda.",
    version="0.2.0",
)

app.include_router(productos.router)
app.include_router(categorias.router)


@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "API Tienda funcionando correctamente"}
