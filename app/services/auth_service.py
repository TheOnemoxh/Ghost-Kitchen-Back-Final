from sqlalchemy.orm import Session
from app.models.user import User, Address
from app.core.security import get_password_hash
# 👇 CORRECCIÓN: Importamos AddressCreate en lugar de AddressBase
from app.schemas.user import UserCreate, AddressCreate, UserUpdate

def crear_usuario(db: Session, user: UserCreate):
    hashed_pwd = get_password_hash(user.password)
    
    db_user = User(
        email=user.email, 
        hashed_password=hashed_pwd, 
        nombre=user.nombre,
        apellido=user.apellido,
        celular=user.celular,
        rol="CLIENTE" # Asignamos rol por defecto
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ...
def agregar_direccion(db: Session, user_id: int, address: AddressCreate):
    # Esto toma todos los campos nuevos (departamento, municipio, etc.) y los pasa al modelo
    db_address = Address(**address.model_dump(), usuario_id=user_id) 
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

#Actualizar usuario
def update_user_profile(
    db: Session,
    current_user: User,
    data: UserUpdate,
) -> User:
    """
    Actualiza los datos básicos del usuario autenticado.
    Solo cambia los campos que vengan en el payload.
    """
    if data.nombre is not None:
        current_user.nombre = data.nombre

    if data.apellido is not None:
        current_user.apellido = data.apellido

    if data.celular is not None:
        current_user.celular = data.celular

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user