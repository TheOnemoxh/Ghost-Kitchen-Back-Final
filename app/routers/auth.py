from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Imports del Core
from app.core.database import get_db
from app.core.security import verify_password, create_access_token, get_current_user # Ahora sí existe
from app.services import auth_service

# Imports de Modelos y Schemas
from app.models.user import User, Address
from app.schemas.user import UserCreate, UserLogin, Token, AddressCreate, AddressResponse

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# --- 1. REGISTRO ---
@router.post("/registro", response_model=Token)
def registrar_usuario(user: UserCreate, db: Session = Depends(get_db)):
    # Validar si existe
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    # Crear usuario (usando tu servicio o directo)
    new_user = auth_service.crear_usuario(db, user)
    
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- 2. LOGIN ---
@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- 3. LISTAR DIRECCIONES ---
@router.get("/direcciones", response_model=List[AddressResponse])
def listar_direcciones(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Filtramos por el usuario que está logueado (current_user)
    return db.query(Address).filter(Address.usuario_id == current_user.id).all()

# --- 4. CREAR DIRECCIÓN ---
@router.post("/direcciones", response_model=AddressResponse)
def crear_direccion(direccion: AddressCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Creamos la dirección vinculada al usuario logueado
    nueva = Address(**direccion.model_dump(), usuario_id=current_user.id) # .model_dump() para Pydantic v2
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

# ... imports anteriores ...

# --- 5. EDITAR DIRECCIÓN (NUEVO) ---
@router.put("/direcciones/{id_direccion}", response_model=AddressResponse)
def editar_direccion(
    id_direccion: int, 
    direccion_update: AddressCreate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    # 1. Buscar la dirección y asegurar que pertenezca al usuario
    address_db = db.query(Address).filter(
        Address.id == id_direccion, 
        Address.usuario_id == current_user.id
    ).first()

    if not address_db:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")

    # 2. Actualizar los campos
    # Usamos model_dump(exclude_unset=True) para solo actualizar lo que enviamos
    update_data = direccion_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(address_db, key, value)

    db.commit()
    db.refresh(address_db)
    return address_db

# --- 6. ELIMINAR DIRECCIÓN (BONUS: Ya que tienes el botón de borrar) ---
@router.delete("/direcciones/{id_direccion}")
def eliminar_direccion(
    id_direccion: int, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    address_db = db.query(Address).filter(
        Address.id == id_direccion, 
        Address.usuario_id == current_user.id
    ).first()

    if not address_db:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")

    db.delete(address_db)
    db.commit()
    return {"mensaje": "Dirección eliminada correctamente"}

from app.schemas.user import UserResponse # <--- Asegúrate de tener este import arriba

# ... (tus otros endpoints login, registro, direcciones) ...

# --- 7. OBTENER PERFIL (NUEVO) ---
@router.get("/me", response_model=UserResponse)
def obtener_perfil(current_user = Depends(get_current_user)):
    """Devuelve los datos del usuario dueño del token"""
    return current_user