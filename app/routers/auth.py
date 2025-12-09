from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Core
from app.core.database import get_db
from app.core.security import (
    verify_password,
    create_access_token,
    get_current_user,
)

# Servicios
from app.services import auth_service

# Modelos SQLAlchemy
from app.models.user import User, Address

# Schemas Pydantic
from app.schemas.user import (
    UserCreate,
    UserLogin,
    Token,
    AddressCreate,
    AddressResponse,
    UserResponse,
    UserUpdate,
)

# ⚠️ SOLO UNA VEZ
router = APIRouter(prefix="/auth", tags=["Autenticación"])

# --- 1. REGISTRO ---
@router.post("/registro", response_model=Token)
def registrar_usuario(user: UserCreate, db: Session = Depends(get_db)):
    # Validar si existe
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    # Crear usuario
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


# --- 3. OBTENER PERFIL ---
@router.get("/me", response_model=UserResponse)
def obtener_perfil(current_user: User = Depends(get_current_user)):
    """Devuelve los datos del usuario dueño del token."""
    return current_user


# --- 4. ACTUALIZAR PERFIL (NUEVO) ---
@router.put("/me", response_model=UserResponse)
def update_me(
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Actualiza nombre, apellido y celular del usuario autenticado.
    Solo cambia los campos que lleguen en el payload.
    """
    updated = auth_service.update_user_profile(
        db=db,
        current_user=current_user,
        data=payload,
    )
    return updated


# --- 5. LISTAR DIRECCIONES ---
@router.get("/direcciones", response_model=List[AddressResponse])
def listar_direcciones(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Address)
        .filter(Address.usuario_id == current_user.id)
        .all()
    )


# --- 6. CREAR DIRECCIÓN ---
@router.post("/direcciones", response_model=AddressResponse)
def crear_direccion(
    direccion: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    nueva = Address(
        **direccion.model_dump(),
        usuario_id=current_user.id,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


# --- 7. EDITAR DIRECCIÓN ---
@router.put("/direcciones/{id_direccion}", response_model=AddressResponse)
def editar_direccion(
    id_direccion: int,
    direccion_update: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    address_db = (
        db.query(Address)
        .filter(
            Address.id == id_direccion,
            Address.usuario_id == current_user.id,
        )
        .first()
    )

    if not address_db:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")

    update_data = direccion_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(address_db, key, value)

    db.commit()
    db.refresh(address_db)
    return address_db


# --- 8. ELIMINAR DIRECCIÓN ---
@router.delete("/direcciones/{id_direccion}")
def eliminar_direccion(
    id_direccion: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    address_db = (
        db.query(Address)
        .filter(
            Address.id == id_direccion,
            Address.usuario_id == current_user.id,
        )
        .first()
    )

    if not address_db:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")

    db.delete(address_db)
    db.commit()
    return {"mensaje": "Dirección eliminada correctamente"}
