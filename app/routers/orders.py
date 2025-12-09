from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import order_service
from app.schemas.order import OrderCreate, OrderResponse, OrderHistory, OrderFullDetail
from app.models.user import User
from app.core.security import get_current_user # 👈 IMPORTANTE

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

# 1. CREAR PEDIDO
@router.post("/", response_model=OrderResponse)
def registrar_pedido(
    pedido: OrderCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # 👈 Token Requerido
):
    # Pasamos el ID real
    return order_service.crear_pedido(db, pedido, current_user.id)

# 2. VER HISTORIAL
@router.get("/historial", response_model=List[OrderHistory])
def ver_historial(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # 👈 Token Requerido
):
    return order_service.obtener_historial_cliente(db, current_user.id)

# 3. ULTIMO ACTIVO
@router.get("/ultimo-activo")
def ver_ultimo_pedido_activo(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # 👈 Token Requerido
):
    return order_service.obtener_ultimo_pedido_activo(db, current_user.id)

# 4. DETALLE
@router.get("/{id_pedido}", response_model=OrderFullDetail)
def ver_detalle_pedido(
    id_pedido: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # 👈 Token Requerido
):
    detalle = order_service.obtener_detalle_pedido(db, id_pedido, current_user.id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return detalle

# 5. CANCELAR
@router.post("/{id_pedido}/cancel")
def cancelar_pedido_endpoint(
    id_pedido: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # 👈 Token Requerido
):
    return order_service.cancelar_pedido(db, id_pedido, current_user.id)