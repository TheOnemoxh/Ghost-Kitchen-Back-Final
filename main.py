from fastapi import FastAPI
from app.core.database import engine, Base
# 1. Importar todos los routers
from app.routers import auth, orders, kitchens, menu, pqr 

# 2. Crear las tablas en la BD
Base.metadata.create_all(bind=engine)

# 3. Inicializar la aplicación (ESTO DEBE IR ANTES DE LOS INCLUDE)
app = FastAPI(title="Ghost Kitchens API")

# 4. Registrar los routers
app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(kitchens.router)
app.include_router(menu.router)
app.include_router(pqr.router)  # <--- Aquí está el de PQR

@app.get("/")
def root():
    return {"message": "API Ghost Kitchens funcionando en Docker!"}