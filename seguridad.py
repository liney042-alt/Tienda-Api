from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from database import obtener_conexion

SECRET_KEY = "clave-super-secreta-de-mas-de-32-caracteres-cambieme"
ALGORITMO = "HS256"
MINUTOS_EXPIRACION = 30


def hashear_password(password: str) -> str:
    hasheado = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hasheado.decode()


def verificar_password(plano: str, hasheado: str) -> bool:
    return bcrypt.checkpw(plano.encode(), hasheado.encode())


def buscar_usuario(username: str):
    conexion = obtener_conexion()
    try:
        fila = conexion.execute(
            """
            SELECT id, username, nombre, password, rol
            FROM usuarios
            WHERE username = ?
            """,
            (username,),
        ).fetchone()
        return dict(fila) if fila else None
    finally:
        conexion.close()


def crear_token(username: str) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_EXPIRACION)
    datos = {"sub": username, "exp": expira}
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITMO)


oauth2_esquema = OAuth2PasswordBearer(tokenUrl="auth/login")


def obtener_usuario_actual(token: str = Depends(oauth2_esquema)):
    error = HTTPException(
        status_code=401,
        detail="Token invalido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        datos = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITMO])
        username = datos.get("sub")
        if username is None:
            raise error
    except jwt.PyJWTError:
        raise error

    usuario = buscar_usuario(username)
    if usuario is None:
        raise error
    return usuario


def requerir_admin(usuario: dict = Depends(obtener_usuario_actual)):
    if usuario["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Requiere rol de administrador")
    return usuario
