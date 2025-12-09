from sqlalchemy.orm import Session
from app.models.pqr import PQR
from app.models.order import Order
from app.schemas.pqr import PQRCreate
from fastapi import HTTPException

def crear_reclamo(db: Session, pqr_data: PQRCreate, user_id: int):
    # 1. Validar que el pedido exista y sea de este usuario
    pedido = db.query(Order).filter(Order.id == pqr_data.pedido_id, Order.cliente_id == user_id).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="El pedido no existe o no te pertenece")

    # 2. Crear la PQR
    nueva_pqr = PQR(
        cliente_id=user_id,
        pedido_id=pqr_data.pedido_id,
        motivo=pqr_data.motivo,
        descripcion=pqr_data.descripcion,
        estado="Abierto"
    )
    
    db.add(nueva_pqr)
    db.commit()
    db.refresh(nueva_pqr)
    return nueva_pqr

def obtener_mis_pqrs(db: Session, user_id: int):
    # Ordenar por fecha descendente (lo más nuevo arriba)
    return db.query(PQR).filter(PQR.cliente_id == user_id).order_by(PQR.fecha_registro.desc()).all()

def obtener_detalle_pqr(db: Session, pqr_id: int, user_id: int):
    # Buscar PQR por ID y asegurar que sea del usuario
    pqr = db.query(PQR).filter(PQR.id == pqr_id, PQR.cliente_id == user_id).first()
    return pqr