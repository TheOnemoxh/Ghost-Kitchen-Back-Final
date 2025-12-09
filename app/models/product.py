from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey

from sqlalchemy.orm import relationship

from app.core.database import Base



class Kitchen(Base):

    __tablename__ = "cocinas"

   

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String)

    imagen_url = Column(String)

    descripcion = Column(String) # Ej: "Comida rápida y hamburguesas"

    ubicacion = Column(String)   # Ej: "Bocagrande, Carrera 3"

    estado = Column(Boolean, default=True)

   

    productos = relationship("Product", back_populates="cocina")



class Product(Base):

    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)

    cocina_id = Column(Integer, ForeignKey("cocinas.id"))

    nombre = Column(String)

    precio = Column(Float)

    descripcion = Column(String)
    imagen_url = Column(String, nullable=True)

    disponible = Column(Boolean, default=True)

   

    cocina = relationship("Kitchen", back_populates="productos")



