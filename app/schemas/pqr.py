from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# --- Para crear una PQR (Pantalla 1) ---
class PQRCreate(BaseModel):
    pedido_id: int
    motivo: str
    descripcion: str

# --- Para el Listado/Historial (Pantalla 2) ---
class PQRListado(BaseModel):
    id: int
    pedido_id: int
    motivo: str
    estado: str # Para el color del badge (Abierto, etc)
    fecha_registro: datetime

    class Config:
        orm_mode = True

# --- Para el Detalle Completo (Pantalla 3) ---
class PQRDetalle(BaseModel):
    id: int
    pedido_id: int
    motivo: str
    descripcion: str
    estado: str
    fecha_registro: datetime
    # Aquí podrías agregar una lista de respuestas/historial en el futuro
    
    class Config:
        orm_mode = True