import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://ghost_user:ghost_password@localhost/ghost_kitchen_db"
)

# Configuración agresiva para alto tráfico
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=500,        # Conexiones base
    max_overflow=500,     # Conexiones de emergencia (Total: 100 simultáneas)
    pool_timeout=120,    # Dale hasta 2 minutos a la fila para responder bajo estrés extremo
    pool_recycle=1800,   # Reinicia conexiones cada 30 min para evitar desconexiones fantasma de red
    pool_pre_ping=True   # Verifica que la conexión esté viva antes de usarla (Evita fallos en picos)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
