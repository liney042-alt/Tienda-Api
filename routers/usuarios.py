from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from database import obtener_conexion
import seguridad

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


class UsuarioActualizar(BaseModel):
    nombre: str


@router.get("")
def listar_usuarios(admin: dict = Depends(seguridad.requerir_admin)):
    conexion = obtener_conexion()
    try:
        filas = conexion.execute(
            """
            SELECT id, username, nombre, rol
            FROM usuarios
            ORDER BY id
            """
        ).fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.get("/{username}")
def obtener_usuario(username: str, admin: dict = Depends(seguridad.requerir_admin)):
    conexion = obtener_conexion()
    try:
        fila = conexion.execute(
            """
            SELECT id, username, nombre, rol
            FROM usuarios
            WHERE username = ?
            """,
            (username,),
        ).fetchone()
        if fila:
            return dict(fila)
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    finally:
        conexion.close()


@router.put("/perfil")
def actualizar_perfil(
    datos: UsuarioActualizar,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            UPDATE usuarios
            SET nombre = ?
            WHERE username = ?
            """,
            (datos.nombre, usuario["username"]),
        )
        conexion.commit()
        return {
            "mensaje": "Perfil actualizado exitosamente",
            "usuario": {
                "username": usuario["username"],
                "nombre": datos.nombre,
                "rol": usuario["rol"],
            },
        }
    finally:
        conexion.close()


@router.delete("/{username}")
def eliminar_usuario(username: str, admin: dict = Depends(seguridad.requerir_admin)):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM usuarios WHERE username = ?", (username,))
        conexion.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"mensaje": f"Usuario '{username}' eliminado exitosamente"}
    finally:
        conexion.close()
