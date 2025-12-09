from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import order_service
from app.schemas.order import OrderCreate, OrderResponse, OrderHistory, OrderFullDetail

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

# 1. CREAR PEDIDO
@router.post("/", response_model=OrderResponse)
def registrar_pedido(pedido: OrderCreate, db: Session = Depends(get_db)):
    user_id_simulado = 1 
    return order_service.crear_pedido(db, pedido, user_id_simulado)

# 2. VER HISTORIAL
@router.get("/historial", response_model=List[OrderHistory])
def ver_historial(db: Session = Depends(get_db)):
    user_id_simulado = 1 
    return order_service.obtener_historial_cliente(db, user_id_simulado)

# ---------------------------------------------------------
# 🔥 IMPORTANTE: ESTA RUTA DEBE IR ANTES DE "/{id_pedido}"
# ---------------------------------------------------------
@router.get("/ultimo-activo")
def ver_ultimo_pedido_activo(db: Session = Depends(get_db)):
    """
    Devuelve el ID del último pedido en curso.
    """
    user_id_simulado = 1
    return order_service.obtener_ultimo_pedido_activo(db, user_id_simulado)

# 3. VER DETALLE (Recibe un ID entero)
# Como esta ruta acepta "cualquier cosa" como ID, debe ir al final de los GETs
@router.get("/{id_pedido}", response_model=OrderFullDetail)
def ver_detalle_pedido(id_pedido: int, db: Session = Depends(get_db)):
    user_id_simulado = 1
    detalle = order_service.obtener_detalle_pedido(db, id_pedido, user_id_simulado)
    if not detalle:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return detalle

# 4. CANCELAR
@router.post("/{id_pedido}/cancel")
def cancelar_pedido_endpoint(id_pedido: int, db: Session = Depends(get_db)):
    user_id_simulado = 1
    return order_service.cancelar_pedido(db, id_pedido, user_id_simulado)