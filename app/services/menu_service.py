from sqlalchemy.orm import Session
from app.models.product import Product

def obtener_productos(db: Session):
    return db.query(Product).filter(Product.disponible == True).all()

def obtener_producto_detalle(db: Session, producto_id: int):
    return db.query(Product).filter(Product.id == producto_id).first()

from sqlalchemy.orm import Session
from app.models.product import Product, Kitchen

def obtener_producto_por_id(db: Session, product_id: int):
    # Buscamos el producto
    producto = db.query(Product).filter(Product.id == product_id).first()
    
    if not producto:
        return None
    
    # Truco de SQLAlchemy: Como tenemos la relación definida en el modelo,
    # podemos acceder a producto.cocina.nombre directamente.
    # Pero para que Pydantic lo lea fácil, podemos retornar el objeto producto
    # y Pydantic se encargará de mapear los datos si la relación está cargada.
    
    # Para asegurar que el schema reciba "cocina_nombre", podemos hacerlo explícito
    # o dejar que el ORM lo maneje. Vamos a dejar que el Router lo formatee para mayor control.
    return producto