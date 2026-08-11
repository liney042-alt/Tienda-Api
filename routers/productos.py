from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from database import obtener_conexion
import seguridad

router = APIRouter(prefix="/productos", tags=["Productos"])


class ProductoEntrada(BaseModel):
    nombre: str
    precio: float
    categoria_id: int


def categoria_existe(categoria_id: int) -> bool:
    conexion = obtener_conexion()
    try:
        fila = conexion.execute(
            "SELECT id FROM categorias WHERE id = ?",
            (categoria_id,),
        ).fetchone()
        return fila is not None
    finally:
        conexion.close()


@router.get("")
def listar_productos():
    conexion = obtener_conexion()
    try:
        filas = conexion.execute(
            """
            SELECT p.id, p.nombre, p.precio, p.categoria_id, c.nombre AS categoria
            FROM productos p
            JOIN categorias c ON c.id = p.categoria_id
            ORDER BY p.id
            """
        ).fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.get("/{producto_id}")
def obtener_producto(producto_id: int):
    conexion = obtener_conexion()
    try:
        fila = conexion.execute(
            """
            SELECT p.id, p.nombre, p.precio, p.categoria_id, c.nombre AS categoria
            FROM productos p
            JOIN categorias c ON c.id = p.categoria_id
            WHERE p.id = ?
            """,
            (producto_id,),
        ).fetchone()
        if fila is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return dict(fila)
    finally:
        conexion.close()


@router.post("", status_code=201)
def crear_producto(
    datos: ProductoEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    if not categoria_existe(datos.categoria_id):
        raise HTTPException(status_code=400, detail="La categoria indicada no existe")

    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            INSERT INTO productos (nombre, precio, categoria_id)
            VALUES (?, ?, ?)
            """,
            (datos.nombre, datos.precio, datos.categoria_id),
        )
        conexion.commit()
        nuevo = {
            "id": cursor.lastrowid,
            "nombre": datos.nombre,
            "precio": datos.precio,
            "categoria_id": datos.categoria_id,
        }
        return {
            "mensaje": "Producto creado",
            "producto": nuevo,
            "creado_por": usuario["username"],
        }
    finally:
        conexion.close()


@router.put("/{producto_id}")
def actualizar_producto(
    producto_id: int,
    datos: ProductoEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    if not categoria_existe(datos.categoria_id):
        raise HTTPException(status_code=400, detail="La categoria indicada no existe")

    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            UPDATE productos
            SET nombre = ?, precio = ?, categoria_id = ?
            WHERE id = ?
            """,
            (datos.nombre, datos.precio, datos.categoria_id, producto_id),
        )
        conexion.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        return {
            "mensaje": f"Producto {producto_id} actualizado",
            "actualizado_por": usuario["username"],
        }
    finally:
        conexion.close()


@router.delete("/{producto_id}")
def eliminar_producto(
    producto_id: int,
    admin: dict = Depends(seguridad.requerir_admin),
):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
        conexion.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        return {
            "mensaje": f"Producto {producto_id} eliminado",
            "eliminado_por": admin["username"],
        }
    finally:
        conexion.close()
