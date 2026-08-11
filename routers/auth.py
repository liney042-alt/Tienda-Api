from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

import seguridad

router = APIRouter(prefix="/auth", tags=["Autenticacion"])


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
