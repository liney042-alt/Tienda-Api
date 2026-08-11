from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

import seguridad

router = APIRouter(prefix="/categorias", tags=["Categorias"])


class CategoriaEntrada(BaseModel):
    nombre: str


categorias = [
    {"id": 1, "nombre": "Perifericos"},
    {"id": 2, "nombre": "Pantallas"},
]


@router.get("")
def listar_categorias():
    return categorias


@router.get("/{categoria_id}")
def obtener_categoria(categoria_id: int):
    for categoria in categorias:
        if categoria["id"] == categoria_id:
            return categoria
    raise HTTPException(status_code=404, detail="Categoria no encontrada")


@router.post("", status_code=201)
def crear_categoria(
    datos: CategoriaEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    nueva_categoria = {"id": len(categorias) + 1, "nombre": datos.nombre}
    categorias.append(nueva_categoria)
    return {
        "mensaje": "Categoria creada",
        "categoria": nueva_categoria,
        "creada_por": usuario["username"],
    }


@router.put("/{categoria_id}")
def actualizar_categoria(
    categoria_id: int,
    datos: CategoriaEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    for categoria in categorias:
        if categoria["id"] == categoria_id:
            categoria["nombre"] = datos.nombre
            return {
                "mensaje": f"Categoria {categoria_id} actualizada",
                "categoria": categoria,
                "actualizada_por": usuario["username"],
            }
    raise HTTPException(status_code=404, detail="Categoria no encontrada")


@router.delete("/{categoria_id}")
def eliminar_categoria(
    categoria_id: int,
    admin: dict = Depends(seguridad.requerir_admin),
):
    for indice, categoria in enumerate(categorias):
        if categoria["id"] == categoria_id:
            categorias.pop(indice)
            return {
                "mensaje": f"Categoria {categoria_id} eliminada",
                "eliminada_por": admin["username"],
            }
    raise HTTPException(status_code=404, detail="Categoria no encontrada")
