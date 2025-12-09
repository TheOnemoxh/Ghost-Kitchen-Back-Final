from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import verify_password, create_access_token, get_current_user
from app.services import auth_service
from app.models.user import User, Address
from app.schemas.user import (
    UserCreate, UserLogin, Token, AddressCreate, 
    AddressResponse, UserResponse, UserUpdate
)

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# --- 1. REGISTRO ---
@router.post("/registro", response_model=Token)
def registrar_usuario(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
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

# --- 3. PERFIL ---
@router.get("/me", response_model=UserResponse)
def obtener_perfil(current_user: User = Depends(get_current_user)):
    return current_user

# --- 4. ACTUALIZAR PERFIL ---
@router.put("/me", response_model=UserResponse)
def update_me(payload: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return auth_service.update_user_profile(db=db, current_user=current_user, data=payload)

# --- 5. LISTAR DIRECCIONES (Corregido) ---
@router.get("/direcciones", response_model=List[AddressResponse])
def listar_direcciones(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 👇 FILTRA SOLO LAS DIRECCIONES DEL USUARIO ACTUAL
    return db.query(Address).filter(Address.usuario_id == current_user.id).all()

# --- 6. CREAR DIRECCIÓN (Corregido) ---
@router.post("/direcciones", response_model=AddressResponse)
def crear_direccion(direccion: AddressCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    nueva = Address(**direccion.model_dump(), usuario_id=current_user.id) # 👈 Usa ID real
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

# ... (Editar y Eliminar siguen la misma lógica, usando current_user.id en el filtro)