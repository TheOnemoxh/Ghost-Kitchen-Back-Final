import sys
import os

# Asegurar que Python encuentre los módulos de la app
sys.path.append(os.getcwd())

from app.core.database import SessionLocal
from app.models.product import Kitchen, Product 

def seed_full_data():
    db = SessionLocal()
    
    print("🧹 Limpiando base de datos antigua...")
    try:
        db.query(Product).delete()
        db.query(Kitchen).delete()
        db.commit()
    except Exception as e:
        print(f"Nota: No se pudo limpiar o estaba vacía ({e})")
        db.rollback()

    print("🌱 Creando Cocinas y Menús con IMÁGENES REALES (Verificadas)...")

    # --- URLs ESTABLES DE UNSPLASH ---
    cocinas_data = [
        {
            "nombre": "Ghost Burger 👻",
            # Foto de portada: Hamburguesa grande
            "imagen": "https://images.unsplash.com/photo-1550547660-d9450f859349?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
            "descripcion": "Las mejores hamburguesas a la parrilla.",
            "ubicacion": "Bocagrande, Carrera 3",
            "menu": [
                {
                    "nombre": "Ghost Classic", 
                    "precio": 22000, 
                    "desc": "Carne 180g, queso cheddar, tocineta.", 
                    # Foto: Hamburguesa clásica
                    "imagen_producto": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                },
                {
                    "nombre": "Doble Muerte", 
                    "precio": 32000, 
                    "desc": "Doble carne, doble queso, aros de cebolla.", 
                    # Foto: Hamburguesa doble
                    "imagen_producto": "https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                },
                {
                    "nombre": "Papas Fantasma", 
                    "precio": 12000, 
                    "desc": "Papas rústicas con paprika.", 
                    # Foto: Papas fritas
                    "imagen_producto": "https://images.unsplash.com/photo-1573080496987-a199f8cd75c5?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                },
                {
                    "nombre": "Coca Cola", 
                    "precio": 5000, 
                    "desc": "Lata 330ml fría.", 
                    # Foto: Refresco
                    "imagen_producto": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                }
            ]
        },
        {
            "nombre": "Pizza Planet 🍕",
            # Foto: Pizza Pepperoni
            "imagen": "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
            "descripcion": "Masa madre y horno de leña.",
            "ubicacion": "Centro Histórico",
            "menu": [
                {
                    "nombre": "Pepperoni Lover", 
                    "precio": 35000, 
                    "desc": "Extra pepperoni, queso mozzarella.", 
                    "imagen_producto": "https://images.unsplash.com/photo-1628840042765-356cda07504e?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                },
                {
                    "nombre": "Hawaiana", 
                    "precio": 32000, 
                    "desc": "Jamón y piña calada.", 
                    "imagen_producto": "https://images.unsplash.com/photo-1513104890138-7c749659a591?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                }
            ]
        },
        {
            "nombre": "Sushi Master 🍣",
            # Foto: Tabla de Sushi
            "imagen": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
            "descripcion": "Auténtica comida japonesa.",
            "ubicacion": "Manga",
            "menu": [
                {
                    "nombre": "Philadelphia Roll", 
                    "precio": 28000, 
                    "desc": "Salmón y queso crema.", 
                    "imagen_producto": "https://images.unsplash.com/photo-1611143669185-af224c5e3252?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                },
                {
                    "nombre": "Ramen", 
                    "precio": 25000, 
                    "desc": "Caldo de cerdo y fideos.", 
                    "imagen_producto": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                }
            ]
        }
    ]

    for k_data in cocinas_data:
        # 1. Crear Cocina
        nueva_cocina = Kitchen(
            nombre=k_data["nombre"],
            imagen_url=k_data["imagen"],
            descripcion=k_data["descripcion"],
            ubicacion=k_data["ubicacion"],
            estado=True
        )
        db.add(nueva_cocina)
        db.commit()
        db.refresh(nueva_cocina)
        
        print(f"🍳 Cocina creada: {nueva_cocina.nombre}")

        # 2. Crear Productos
        for p_data in k_data["menu"]:
            nuevo_producto = Product(
                nombre=p_data["nombre"],
                precio=p_data["precio"],
                descripcion=p_data["desc"],
                disponible=True,
                imagen_url=p_data["imagen_producto"], 
                cocina_id=nueva_cocina.id
            )
            db.add(nuevo_producto)
        
        db.commit()

    print("✅ ¡Base de datos actualizada con imágenes funcionales!")
    db.close()

if __name__ == "__main__":
    seed_full_data()