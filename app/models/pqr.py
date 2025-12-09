from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class PQR(Base):
    __tablename__ = "pqrs"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"))
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    
    # Datos del formulario
    motivo = Column(String) # Ej: "Pedido incompleto"
    descripcion = Column(Text) # Descripción detallada
    
    # Datos del sistema
    estado = Column(String, default="Abierto") # Abierto, En proceso, Cerrado
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    cliente = relationship("User") # Si quieres acceder a datos del cliente
    pedido = relationship("Order") # Para mostrar "Pedido asociado: #3"