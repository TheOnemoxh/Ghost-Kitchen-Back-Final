from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from enum import Enum

# Definimos los estados exactos que usará el Frontend para la línea de tiempo
class OrderStatus(str, Enum):
    CONFIRMED = "CONFIRMED"     # Confirmado (Estado 1)
    PREPARING = "PREPARING"     # En preparación (Estado 2)
    ON_WAY = "ON_WAY"           # En camino (Estado 3)
    DELIVERED = "DELIVERED"     # Entregado (Estado 4)
    CANCELLED = "CANCELLED"     # Cancelado (Estado especial)

class Order(Base):
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"))
    
    # Por defecto el pedido nace como CONFIRMED
    estado = Column(String, default=OrderStatus.CONFIRMED.value) 
    total = Column(Float, default=0.0)
    fecha = Column(DateTime, default=datetime.utcnow)
    
    # Campos de pago
    metodo_pago = Column(String) 
    id_transaccion = Column(String, nullable=True)
    
    cliente = relationship("User", back_populates="pedidos")
    detalles = relationship("OrderDetail", back_populates="pedido")

class OrderDetail(Base):
    __tablename__ = "detalle_pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer)
    precio_unitario = Column(Float)
    
    pedido = relationship("Order", back_populates="detalles")
    producto = relationship("Product")