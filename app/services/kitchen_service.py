from sqlalchemy.orm import Session
from app.models.product import Kitchen

def obtener_cocinas_todas(db: Session):
    return db.query(Kitchen).filter(Kitchen.estado == True).all()

# ... (imports existentes)

def obtener_cocina_por_id(db: Session, kitchen_id: int):
    # Busca la cocina por ID
    # SQLAlchemy traerá automáticamente la relación "productos" 
    # cuando el Schema de Pydantic lo solicite.
    return db.query(Kitchen).filter(Kitchen.id == kitchen_id).first()