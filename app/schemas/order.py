from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from enum import Enum

# --- ENUMS ---
class MetodoPago(str, Enum):
    EFECTIVO = "EFECTIVO"
    DATAFONO = "DATAFONO"
    LINEA = "LINEA"

# --- INPUTS (Frontend -> Backend) ---
class OrderItemCreate(BaseModel):
    producto_id: int
    cantidad: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    direccion_id: int  # 👈 NUEVO CAMPO OBLIGATORIO
    metodo_pago: MetodoPago 

# --- OUTPUTS (Backend -> Frontend) ---

class OrderResponse(BaseModel):
    id: int
    estado: str
    total: float
    metodo_pago: str
    id_transaccion: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class OrderHistory(BaseModel):
    id: int
    fecha: datetime
    total: float
    estado: str
    metodo_pago: str
    cantidad_items: int
    model_config = ConfigDict(from_attributes=True)

class DetalleItemView(BaseModel):
    producto_nombre: str
    cantidad: int
    precio_unitario: float
    subtotal: float
    imagen_producto: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class OrderFullDetail(BaseModel):
    id: int
    fecha: datetime
    estado: str
    total: float
    metodo_pago: str
    id_transaccion: Optional[str] = None
    items: List[DetalleItemView] = []
    
    # Opcional: Si quisieras devolver la dirección en el detalle en el futuro
    # direccion: Optional[AddressDto] = None 
    
    model_config = ConfigDict(from_attributes=True)