# API Tienda - FastAPI

Proyecto de aprendizaje para construir una API REST de una tienda con FastAPI.

## Guia 1

- Creacion de la aplicacion FastAPI.
- Endpoint raiz.
- Endpoints de consulta para productos.
- Parametros de ruta y parametros de consulta.

## Guia 2

- Organizacion del proyecto con `APIRouter`.
- CRUD completo para productos.
- CRUD completo para categorias.
- Modelos de entrada con Pydantic.

## Guia 3

- Login con OAuth2 y JWT.
- Hashing de contrasenas con bcrypt.
- Endpoints protegidos con `Depends`.
- Autorizacion por rol administrador.

## Ejecutar

```bash
pip install fastapi "uvicorn[standard]"
uvicorn main:app --reload
```

La documentacion interactiva queda disponible en:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc
