from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import pqr_service
from app.schemas.pqr import PQRCreate, PQRListado, PQRDetalle
from app.models.user import User
from app.core.security import get_current_user # 👈 IMPORTANTE

router = APIRouter(prefix="/pqr", tags=["Soporte y PQR"])

@router.post("/", response_model=PQRListado)
def registrar_pqr(
    pqr: PQRCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # 👈 Token
):
    return pqr_service.crear_reclamo(db, pqr, user_id=current_user.id)

@router.get("/historial", response_model=List[PQRListado])
def ver_historial_pqrs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # 👈 Token
):
    return pqr_service.obtener_mis_pqrs(db, user_id=current_user.id)

@router.get("/{id_pqr}", response_model=PQRDetalle)
def ver_detalle_pqr(
    id_pqr: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # 👈 Token
):
    pqr = pqr_service.obtener_detalle_pqr(db, id_pqr, user_id=current_user.id)
    if not pqr:
        raise HTTPException(status_code=404, detail="PQR no encontrada")
    return pqr