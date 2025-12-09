from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import order_service
# Importamos TODOS los esquemas necesarios
from app.schemas.order import OrderCreate, OrderResponse, OrderHistory, OrderFullDetail

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

# 1. CREAR PEDIDO (POST /pedidos/)
@router.post("/", response_model=OrderResponse)
def registrar_pedido(pedido: OrderCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo pedido.
    Si el método de pago es 'LINEA', simula la pasarela de pagos.
    """
    # Simulamos usuario ID 1 temporalmente
    user_id_simulado = 1 
    return order_service.crear_pedido(db, pedido, user_id_simulado)

# 2. VER HISTORIAL (GET /pedidos/historial)
@router.get("/historial", response_model=List[OrderHistory])
def ver_historial(db: Session = Depends(get_db)):
    """
    Obtiene la lista de pedidos del usuario logueado.
    Muestra: Fecha, Total, Estado y Método de Pago.
    """
    user_id_simulado = 1 
    return order_service.obtener_historial_cliente(db, user_id_simulado)

# 3. VER DETALLE (GET /pedidos/{id})
@router.get("/{id_pedido}", response_model=OrderFullDetail)
def ver_detalle_pedido(id_pedido: int, db: Session = Depends(get_db)):
    """
    Muestra el recibo completo de un pedido específico.
    Incluye la lista de productos comprados.
    """
    user_id_simulado = 1
    
    detalle = order_service.obtener_detalle_pedido(db, id_pedido, user_id_simulado)
    
    if not detalle:
        raise HTTPException(status_code=404, detail="Pedido no encontrado o no te pertenece")
        
    return detalle

# ---------------------------------------------------------
# 4. CANCELAR PEDIDO (POST /pedidos/{id}/cancel) - ¡NUEVO!
# ---------------------------------------------------------
@router.post("/{id_pedido}/cancel")
def cancelar_pedido_endpoint(id_pedido: int, db: Session = Depends(get_db)):
    """
    Cancela un pedido si todavía está en estado CONFIRMED.
    """
    user_id_simulado = 1
    # Llamamos a la función nueva que creamos en el servicio
    return order_service.cancelar_pedido(db, id_pedido, user_id_simulado)