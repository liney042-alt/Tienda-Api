from fastapi import FastAPI

app = FastAPI(
    title="API Tienda",
    description="Primera API de tienda construida con FastAPI.",
    version="0.1.0",
)

productos = [
    {"id": 1, "nombre": "Teclado mecanico", "precio": 120000, "categoria": "Perifericos"},
    {"id": 2, "nombre": "Mouse gamer", "precio": 85000, "categoria": "Perifericos"},
    {"id": 3, "nombre": "Monitor 24", "precio": 650000, "categoria": "Pantallas"},
]


@app.get("/")
def inicio():
    return {"mensaje": "Mi primera API con FastAPI"}


@app.get("/productos")
def listar_productos():
    return productos


@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int):
    for producto in productos:
        if producto["id"] == producto_id:
            return producto
    return {"mensaje": "Producto no encontrado"}


@app.get("/buscar")
def buscar_productos(categoria: str | None = None, precio_max: float | None = None):
    resultados = productos

    if categoria:
        resultados = [
            producto for producto in resultados
            if producto["categoria"].lower() == categoria.lower()
        ]

    if precio_max:
        resultados = [
            producto for producto in resultados
            if producto["precio"] <= precio_max
        ]

    return resultados
