from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from enum import Enum

class OrderStatus(str, Enum):
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    ON_WAY = "ON_WAY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class Order(Base):
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"))
    
    # 👇 ESTE ES EL CAMBIO CLAVE: Relación con la tabla de direcciones
    direccion_id = Column(Integer, ForeignKey("direcciones.id"), nullable=True)

    # Por defecto el pedido nace como CONFIRMED
    estado = Column(String, default=OrderStatus.CONFIRMED.value) 
    total = Column(Float, default=0.0)
    fecha = Column(DateTime, default=datetime.utcnow)
    
    # Campos de pago
    metodo_pago = Column(String) 
    id_transaccion = Column(String, nullable=True)
    
    # Relaciones
    # Usamos string "User" y "Address" para evitar errores de importación circular
    cliente = relationship("User", back_populates="pedidos")
    detalles = relationship("OrderDetail", back_populates="pedido")
    
    # 👇 Relación para poder hacer order.direccion.direccion_exacta
    direccion = relationship("Address")

class OrderDetail(Base):
    __tablename__ = "detalle_pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer)
    precio_unitario = Column(Float)
    
    pedido = relationship("Order", back_populates="detalles")
    producto = relationship("Product")