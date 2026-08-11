from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

import seguridad

router = APIRouter(prefix="/productos", tags=["Productos"])


class ProductoEntrada(BaseModel):
    nombre: str
    precio: float
    categoria: str


productos = [
    {"id": 1, "nombre": "Teclado mecanico", "precio": 120000, "categoria": "Perifericos"},
    {"id": 2, "nombre": "Mouse gamer", "precio": 85000, "categoria": "Perifericos"},
    {"id": 3, "nombre": "Monitor 24", "precio": 650000, "categoria": "Pantallas"},
]


@router.get("")
def listar_productos():
    return productos


@router.get("/{producto_id}")
def obtener_producto(producto_id: int):
    for producto in productos:
        if producto["id"] == producto_id:
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")


@router.post("", status_code=201)
def crear_producto(
    datos: ProductoEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    nuevo_producto = {"id": len(productos) + 1, **datos.model_dump()}
    productos.append(nuevo_producto)
    return {
        "mensaje": "Producto creado",
        "producto": nuevo_producto,
        "creado_por": usuario["username"],
    }


@router.put("/{producto_id}")
def actualizar_producto(
    producto_id: int,
    datos: ProductoEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    for producto in productos:
        if producto["id"] == producto_id:
            producto.update(datos.model_dump())
            return {
                "mensaje": f"Producto {producto_id} actualizado",
                "producto": producto,
                "actualizado_por": usuario["username"],
            }
    raise HTTPException(status_code=404, detail="Producto no encontrado")


@router.delete("/{producto_id}")
def eliminar_producto(
    producto_id: int,
    admin: dict = Depends(seguridad.requerir_admin),
):
    for indice, producto in enumerate(productos):
        if producto["id"] == producto_id:
            productos.pop(indice)
            return {
                "mensaje": f"Producto {producto_id} eliminado",
                "eliminado_por": admin["username"],
            }
    raise HTTPException(status_code=404, detail="Producto no encontrado")
