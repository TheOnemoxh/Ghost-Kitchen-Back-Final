from pydantic import BaseModel
from typing import List, Optional # <--- Asegúrate de importar Optional
# --- DTO para la tarjeta de cocina simplificada ---
class KitchenCard(BaseModel):
    id: int
    nombre: str
    imagen_url: str
    descripcion: str
    ubicacion: str
    
    class Config:
        orm_mode = True

# --- DTO de Productos (Se mantiene igual) ---
class ProductResponse(BaseModel):
    id: int
    nombre: str
    precio: float
    descripcion: str
    disponible: bool
    imagen_url: Optional[str] = None  # <--- AGREGA ESTA LÍNEA

    class Config:
        orm_mode = True

# ... (imports existentes)
 # Asegúrate de tener esto importado

# ... (KitchenCard y ProductResponse existentes)

# --- NUEVO: DTO para el Detalle de Cocina (Menú) ---
class KitchenDetail(KitchenCard):
    # Hereda nombre, imagen, etc. de KitchenCard
    # Y le agregamos la lista de productos
    productos: List[ProductResponse] = []

    class Config:
        orm_mode = True

# ... imports anteriores

# --- NUEVO: DTO para el Detalle de un Producto individual ---
class ProductDetail(ProductResponse):
    # Hereda id, nombre, precio, descripcion, disponible de ProductResponse
    # Agregamos campos extra útiles para la pantalla de detalle:
    cocina_nombre: str 
    cocina_id: int

    class Config:
        orm_mode = True