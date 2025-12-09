from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    nombre = Column(String)
    apellido = Column(String)
    celular = Column(String)
    rol = Column(String, default="CLIENTE")
    
    # Relaciones
    direcciones = relationship("Address", back_populates="usuario")
    pedidos = relationship("Order", back_populates="cliente")

class Address(Base):
    __tablename__ = "direcciones"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    
    # --- COLUMNAS NUEVAS (Coinciden con el Frontend y el Schema) ---
    direccion_exacta = Column(String)
    departamento = Column(String)
    municipio = Column(String)
    barrio = Column(String)
    apartamento_casa = Column(String, nullable=True)
    indicaciones = Column(String(128), nullable=True)
    
    usuario = relationship("User", back_populates="direcciones")