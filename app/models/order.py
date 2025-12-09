from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Order(Base):
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"))
    
    # Estados: CONFIRMADO, PAGADO, EN_PREPARACION, ETC.
    estado = Column(String, default="PENDIENTE") 
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
    # Relación con producto para poder acceder a sus datos si se necesita
    producto = relationship("Product")