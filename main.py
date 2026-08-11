from fastapi import FastAPI
from routers import auth, categorias, productos, usuarios

app = FastAPI(
    title="API Tienda Segura",
    description="API REST modularizada con autenticacion JWT y control de roles.",
    version="0.3.0",
)

app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(categorias.router)
app.include_router(usuarios.router)


@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "API Tienda Segura funcionando correctamente"}
