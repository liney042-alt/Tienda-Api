from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

import seguridad

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


class UsuarioActualizar(BaseModel):
    nombre: str


@router.get("")
def listar_usuarios(admin: dict = Depends(seguridad.requerir_admin)):
    return [
        {"username": usuario["username"], "nombre": usuario["nombre"], "rol": usuario["rol"]}
        for usuario in seguridad.usuarios
    ]


@router.get("/{username}")
def obtener_usuario(username: str, admin: dict = Depends(seguridad.requerir_admin)):
    usuario = seguridad.buscar_usuario(username)
    if usuario:
        return {
            "username": usuario["username"],
            "nombre": usuario["nombre"],
            "rol": usuario["rol"],
        }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.put("/perfil")
def actualizar_perfil(
    datos: UsuarioActualizar,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    usuario["nombre"] = datos.nombre
    return {
        "mensaje": "Perfil actualizado exitosamente",
        "usuario": {
            "username": usuario["username"],
            "nombre": usuario["nombre"],
            "rol": usuario["rol"],
        },
    }


@router.delete("/{username}")
def eliminar_usuario(username: str, admin: dict = Depends(seguridad.requerir_admin)):
    for indice, usuario in enumerate(seguridad.usuarios):
        if usuario["username"] == username:
            seguridad.usuarios.pop(indice)
            return {"mensaje": f"Usuario '{username}' eliminado exitosamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
