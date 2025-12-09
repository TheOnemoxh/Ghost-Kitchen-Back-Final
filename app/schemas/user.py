from pydantic import BaseModel, ConfigDict
from typing import Optional

# --------------------------------------------------------
# 1. USUARIOS (REGISTRO Y LOGIN)
# --------------------------------------------------------
class UserCreate(BaseModel):
    nombre: str
    apellido: str
    email: str  # Usamos str simple para evitar errores de librerías faltantes
    celular: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    celular: str
    rol: str
    
    # Configuración para Pydantic V2 (lectura desde ORM)
    model_config = ConfigDict(from_attributes=True)

# --------------------------------------------------------
# 2. TOKENS
# --------------------------------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --------------------------------------------------------
# 3. DIRECCIONES (DETALLADAS)
# --------------------------------------------------------
# Este esquema debe coincidir EXACTAMENTE con las columnas de tu BD
class AddressCreate(BaseModel):
    direccion_exacta: str
    departamento: str
    municipio: str
    barrio: str
    apartamento_casa: Optional[str] = None
    indicaciones: Optional[str] = None
    # NOTA: Eliminamos 'alias' porque no está en tu tabla de BD y causaba error.

class AddressResponse(AddressCreate):
    id: int
    usuario_id: int
    
    model_config = ConfigDict(from_attributes=True)