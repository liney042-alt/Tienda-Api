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

## Extra: usuarios

- Registro de clientes.
- Consulta de usuario autenticado.
- Administracion de usuarios para rol administrador.

## Extra: pedidos

- Creacion de pedidos para usuarios autenticados.
- Consulta de pedidos propios para clientes.
- Consulta y eliminacion global para administradores.

## Guia 5

- Persistencia de datos con SQLite3.
- Creacion automatica de `tienda.db` al iniciar la API.
- Tablas `categorias`, `productos` y `usuarios`.
- Consultas SQL parametrizadas con `?` para evitar inyeccion SQL.
- CRUD de categorias con validacion de duplicados, productos asociados y consulta con JOIN.
- Taller independiente de SQL en `taller_sql.py`.

## Ejecutar

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

La documentacion interactiva queda disponible en:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Usuarios de prueba

| Usuario | Contrasena | Rol |
| --- | --- | --- |
| `admin@tienda.com` | `admin123` | admin |
| `ana@tienda.com` | `ana123` | cliente |

## Probar persistencia

1. Inicie el servidor con `uvicorn main:app --reload`.
2. Entre a `http://127.0.0.1:8000/docs`.
3. Inicie sesion en `/auth/login` y copie el token.
4. Use `Authorize` con `Bearer <token>`.
5. Cree un producto en `POST /productos`.
6. Detenga el servidor y vuelva a iniciarlo.
7. Consulte `GET /productos`: el producto debe seguir guardado en `tienda.db`.

## Taller SQL

Ejecute:

```bash
python taller_sql.py
```

El script crea `taller.db`, resuelve los ejercicios de `INSERT`, `SELECT`, `UPDATE`,
`DELETE`, `fetchone`, `fetchall`, `row_factory` y compara una consulta vulnerable
con una consulta parametrizada.
