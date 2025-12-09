from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import menu_service
from app.schemas.product import ProductResponse, ProductDetail

router = APIRouter(prefix="/menu", tags=["Menú y Productos"])

# --- Endpoint para listar todos los productos (opcional, si lo usas) ---
@router.get("/productos", response_model=List[ProductResponse])
def ver_productos(db: Session = Depends(get_db)):
    return menu_service.obtener_productos(db)

# --- Endpoint DETALLE DEL PRODUCTO (Aquí estaba el error) ---
@router.get("/productos/{id}", response_model=ProductDetail)
def ver_detalle_producto(id: int, db: Session = Depends(get_db)):
    """
    Obtiene el detalle de un producto específico.
    Se usa cuando el cliente da click a un plato en la lista.
    """
    producto = menu_service.obtener_producto_por_id(db, id)
    
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Construimos la respuesta combinando datos del producto y su cocina
    return {
        "id": producto.id,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "descripcion": producto.descripcion,
        "disponible": producto.disponible,
        
        # 👇👇👇 ESTA ES LA LÍNEA QUE FALTABA 👇👇👇
        "imagen_url": producto.imagen_url,
        # 👆👆👆 AGREGA ESTO 👆👆👆
        
        "cocina_id": producto.cocina.id,       # Acceso por relación ORM
        "cocina_nombre": producto.cocina.nombre # Acceso por relación ORM
    }