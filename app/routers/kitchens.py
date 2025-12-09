from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import kitchen_service
from app.schemas.product import KitchenCard

router = APIRouter(prefix="/cocinas", tags=["Cocinas (Home)"])

@router.get("/", response_model=List[KitchenCard])
def listar_todas(db: Session = Depends(get_db)):
    """Obtiene el listado de todas las cocinas asociadas"""
    return kitchen_service.obtener_cocinas_todas(db)

from fastapi import APIRouter, Depends, HTTPException # Importar HTTPException
from app.schemas.product import KitchenDetail # Importar el nuevo schema

# ... (router existente)

@router.get("/{id}", response_model=KitchenDetail)
def ver_menu_cocina(id: int, db: Session = Depends(get_db)):
    """
    Obtiene el detalle de una cocina y todos sus productos.
    Se usa cuando el cliente da click en una tarjeta del Home.
    """
    cocina = kitchen_service.obtener_cocina_por_id(db, id)
    
    if not cocina:
        raise HTTPException(status_code=404, detail="Cocina no encontrada")
        
    return cocina