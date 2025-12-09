from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import pqr_service
from app.schemas.pqr import PQRCreate, PQRListado, PQRDetalle

router = APIRouter(prefix="/pqr", tags=["Soporte y PQR"])

@router.post("/", response_model=PQRListado)
def registrar_pqr(pqr: PQRCreate, db: Session = Depends(get_db)):
    """Crea un nuevo ticket de soporte asociado a un pedido"""
    # Usamos user_id=1 simulado. En producción usarás el token.
    return pqr_service.crear_reclamo(db, pqr, user_id=1)

@router.get("/historial", response_model=List[PQRListado])
def ver_historial_pqrs(db: Session = Depends(get_db)):
    """Lista todas las PQRs del usuario (Pantalla Mis PQR)"""
    return pqr_service.obtener_mis_pqrs(db, user_id=1)

@router.get("/{id_pqr}", response_model=PQRDetalle)
def ver_detalle_pqr(id_pqr: int, db: Session = Depends(get_db)):
    """Muestra el detalle completo de una PQR específica"""
    pqr = pqr_service.obtener_detalle_pqr(db, id_pqr, user_id=1)
    if not pqr:
        raise HTTPException(status_code=404, detail="PQR no encontrada")
    return pqr