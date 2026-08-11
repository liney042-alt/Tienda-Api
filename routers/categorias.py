import sqlite3

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from database import obtener_conexion
import seguridad

router = APIRouter(prefix="/categorias", tags=["Categorias"])


class CategoriaEntrada(BaseModel):
    nombre: str
    descripcion: str | None = None


@router.get("")
def listar_categorias():
    conexion = obtener_conexion()
    try:
        filas = conexion.execute(
            "SELECT id, nombre, descripcion FROM categorias ORDER BY id"
        ).fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.get("/{categoria_id}")
def obtener_categoria(categoria_id: int):
    conexion = obtener_conexion()
    try:
        fila = conexion.execute(
            """
            SELECT id, nombre, descripcion
            FROM categorias
            WHERE id = ?
            """,
            (categoria_id,),
        ).fetchone()
        if fila is None:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")
        return dict(fila)
    finally:
        conexion.close()


@router.get("/{categoria_id}/productos")
def obtener_categoria_con_productos(categoria_id: int):
    conexion = obtener_conexion()
    try:
        categoria = conexion.execute(
            """
            SELECT id, nombre, descripcion
            FROM categorias
            WHERE id = ?
            """,
            (categoria_id,),
        ).fetchone()
        if categoria is None:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")

        productos = conexion.execute(
            """
            SELECT p.id, p.nombre, p.precio, p.categoria_id
            FROM productos p
            JOIN categorias c ON c.id = p.categoria_id
            WHERE c.id = ?
            ORDER BY p.id
            """,
            (categoria_id,),
        ).fetchall()

        resultado = dict(categoria)
        resultado["productos"] = [dict(producto) for producto in productos]
        return resultado
    finally:
        conexion.close()


@router.post("", status_code=201)
def crear_categoria(
    datos: CategoriaEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            INSERT INTO categorias (nombre, descripcion)
            VALUES (?, ?)
            """,
            (datos.nombre, datos.descripcion),
        )
        conexion.commit()
        nueva = {
            "id": cursor.lastrowid,
            "nombre": datos.nombre,
            "descripcion": datos.descripcion,
        }
        return {
            "mensaje": "Categoria creada",
            "categoria": nueva,
            "creada_por": usuario["username"],
        }
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="La categoria ya existe")
    finally:
        conexion.close()


@router.put("/{categoria_id}")
def actualizar_categoria(
    categoria_id: int,
    datos: CategoriaEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            UPDATE categorias
            SET nombre = ?, descripcion = ?
            WHERE id = ?
            """,
            (datos.nombre, datos.descripcion, categoria_id),
        )
        conexion.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")

        return {
            "mensaje": f"Categoria {categoria_id} actualizada",
            "actualizada_por": usuario["username"],
        }
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="La categoria ya existe")
    finally:
        conexion.close()


@router.delete("/{categoria_id}")
def eliminar_categoria(
    categoria_id: int,
    admin: dict = Depends(seguridad.requerir_admin),
):
    conexion = obtener_conexion()
    try:
        productos_asociados = conexion.execute(
            "SELECT COUNT(*) AS total FROM productos WHERE categoria_id = ?",
            (categoria_id,),
        ).fetchone()["total"]
        if productos_asociados > 0:
            raise HTTPException(
                status_code=400,
                detail="No se puede eliminar una categoria con productos asociados",
            )

        cursor = conexion.cursor()
        cursor.execute("DELETE FROM categorias WHERE id = ?", (categoria_id,))
        conexion.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")

        return {
            "mensaje": f"Categoria {categoria_id} eliminada",
            "eliminada_por": admin["username"],
        }
    finally:
        conexion.close()
