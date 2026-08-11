from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

import seguridad

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


class ItemPedido(BaseModel):
    producto_id: int
    cantidad: int


class PedidoEntrada(BaseModel):
    items: List[ItemPedido]


pedidos = [
    {
        "id": 1,
        "usuario": "ana",
        "items": [{"producto_id": 1, "cantidad": 2}],
        "estado": "completado",
    }
]


@router.get("")
def listar_pedidos(usuario: dict = Depends(seguridad.obtener_usuario_actual)):
    if usuario["rol"] == "admin":
        return pedidos

    return [
        pedido for pedido in pedidos
        if pedido["usuario"] == usuario["username"]
    ]


@router.get("/{pedido_id}")
def obtener_pedido(
    pedido_id: int,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    for pedido in pedidos:
        if pedido["id"] == pedido_id:
            if pedido["usuario"] == usuario["username"] or usuario["rol"] == "admin":
                return pedido
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para ver este pedido",
            )
    raise HTTPException(status_code=404, detail="Pedido no encontrado")


@router.post("", status_code=201)
def crear_pedido(
    datos: PedidoEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    nuevo_pedido = {
        "id": len(pedidos) + 1,
        "usuario": usuario["username"],
        "items": [item.model_dump() for item in datos.items],
        "estado": "pendiente",
    }
    pedidos.append(nuevo_pedido)
    return {"mensaje": "Pedido creado exitosamente", "pedido": nuevo_pedido}


@router.delete("/{pedido_id}")
def eliminar_pedido(
    pedido_id: int,
    admin: dict = Depends(seguridad.requerir_admin),
):
    for indice, pedido in enumerate(pedidos):
        if pedido["id"] == pedido_id:
            pedidos.pop(indice)
            return {
                "mensaje": f"Pedido {pedido_id} eliminado exitosamente",
                "eliminado_por": admin["username"],
            }
    raise HTTPException(status_code=404, detail="Pedido no encontrado")
