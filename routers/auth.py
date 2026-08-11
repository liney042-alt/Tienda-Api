import sqlite3

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from database import obtener_conexion
import seguridad

router = APIRouter(prefix="/auth", tags=["Autenticacion"])


class UsuarioRegistro(BaseModel):
    username: str
    nombre: str
    password: str


@router.post("/login")
def login(datos: OAuth2PasswordRequestForm = Depends()):
    usuario = seguridad.buscar_usuario(datos.username)
    if usuario is None or not seguridad.verificar_password(
        datos.password, usuario["password"]
    ):
        raise HTTPException(status_code=401, detail="Usuario o contrasena incorrectos")

    token = seguridad.crear_token(usuario["username"])
    return {"access_token": token, "token_type": "bearer"}


@router.get("/yo")
def quien_soy(usuario: dict = Depends(seguridad.obtener_usuario_actual)):
    return {
        "username": usuario["username"],
        "nombre": usuario["nombre"],
        "rol": usuario["rol"],
    }


@router.post("/registro", status_code=201)
def registrar_usuario(datos: UsuarioRegistro):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            INSERT INTO usuarios (username, nombre, password, rol)
            VALUES (?, ?, ?, ?)
            """,
            (
                datos.username,
                datos.nombre,
                seguridad.hashear_password(datos.password),
                "cliente",
            ),
        )
        conexion.commit()
        return {"mensaje": "Usuario registrado exitosamente", "username": datos.username}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
    finally:
        conexion.close()
