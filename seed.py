from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.kitchen import Kitchen  # Asegúrate que este sea tu modelo de Cocina
from app.models.product import Product  # Asegúrate que este sea tu modelo de Producto

# Datos de prueba (6 Cocinas con Menú)
cocinas_data = [
    {
        "nombre": "Ghost Burger 🍔",
        "descripcion": "Las mejores hamburguesas artesanales a la parrilla.",
        "ubicacion": "Bocagrande, Carrera 3",
        "imagen_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80",
        "productos": [
            {"nombre": "Classic Chesse", "precio": 22000, "descripcion": "Carne 180g, doble cheddar, tocineta.", "imagen_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=500&q=60"},
            {"nombre": "Bacon Master", "precio": 28000, "descripcion": "Doble carne, aros de cebolla, salsa BBQ.", "imagen_url": "https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5?auto=format&fit=crop&w=500&q=60"},
            {"nombre": "Papas Rústicas", "precio": 12000, "descripcion": "Papas con cáscara y paprika.", "imagen_url": "https://images.unsplash.com/photo-1630384060421-a4323ce56d20?auto=format&fit=crop&w=500&q=60"}
        ]
    },
    {
        "nombre": "Pizza Planet 🍕",
        "descripcion": "Masa madre, horno de leña y mucho queso.",
        "ubicacion": "Centro Histórico",
        "imagen_url": "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?auto=format&fit=crop&w=800&q=80",
        "productos": [
            {"nombre": "Pepperoni Lovers", "precio": 35000, "descripcion": "Salsa napolitana y mucho pepperoni.", "imagen_url": "https://images.unsplash.com/photo-1628840042765-356cda07504e?auto=format&fit=crop&w=500&q=60"},
            {"nombre": "Margarita", "precio": 30000, "descripcion": "Albahaca fresca, tomate y mozzarella.", "imagen_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=500&q=60"},
            {"nombre": "Hawillana", "precio": 32000, "descripcion": "Piña caramelizada y jamón.", "imagen_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=500&q=60"}
        ]
    },
    {
        "nombre": "Sushi Master 🍣",
        "descripcion": "Auténtica comida japonesa y fusión.",
        "ubicacion": "Manga, Avenida del Lago",
        "imagen_url": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&w=800&q=80",
        "productos": [
            {"nombre": "California Roll", "precio": 25000, "descripcion": "Cangrejo, aguacate y pepino.", "imagen_url": "https://images.unsplash.com/photo-1617196019294-dcce4789555c?auto=format&fit=crop&w=500&q=60"},
            {"nombre": "Salmon Sashimi", "precio": 18000, "descripcion": "Cortes frescos de salmón.", "imagen_url": "https://images.unsplash.com/photo-1534482421-64566f976cfa?auto=format&fit=crop&w=500&q=60"},
            {"nombre": "Poke Bowl", "precio": 30000, "descripcion": "Arroz, salmón, mango y edamame.", "imagen_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=500&q=60"}
        ]
    },
    {
        "nombre": "El Pollo Hermanos 🍗",
        "descripcion": "El mejor pollo frito crujiente de la ciudad.",
        "ubicacion": "Pie de la Popa",
        "imagen_url": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?auto=format&fit=crop&w=800&q=80",
        "productos": [
            {"nombre": "Combo Familiar", "precio": 45000, "descripcion": "8 presas, papas y gaseosa.", "imagen_url": "https://images.unsplash.com/photo-1562967914-608f82629710?auto=format&fit=crop&w=500&q=60"},
            {"nombre": "Alitas BBQ", "precio": 20000, "descripcion": "10 alitas bañadas en salsa.", "imagen_url": "https://images.unsplash.com/photo-1567620832903-9fc6debc209f?auto=format&fit=crop&w=500&q=60"},
            {"nombre": "Mazorca", "precio": 8000, "descripcion": "Mazorca dulce con mantequilla.", "imagen_url": "https://images.unsplash.com/photo-1551326844-36a5ef81694c?auto=format&fit=crop&w=500&q=60"}
        ]
    },
    {
        "nombre": "Taco Fiesta 🌮",
        "descripcion": "Sabor mexicano picante y delicioso.",
        "ubicacion": "Getsemaní",
        "imagen_url": "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?auto=format&fit=crop&w=800&q=80",
        "productos": [
            {"nombre": "Tacos al Pastor", "precio": 15000, "descripcion": "3 tacos de cerdo marinado con piña.", "imagen_url": "https://images.unsplash.com/photo-1599974579688-8dbdd335c77f?auto=format&fit=crop&w=500&q=60"},
            {"nombre": "Nachos Supremos", "precio": 28000, "descripcion": "Con queso, frijoles y jalapeños.", "imagen_url": "https://images.unsplash.com/photo-1519638399535-1b036603ac77?auto=format&fit=crop&w=500&q=60"},
            {"nombre": "Burrito Mixto", "precio": 22000, "descripcion": "Pollo, carne, arroz y frijol.", "imagen_url": "https://images.unsplash.com/photo-1566740933430-b55593292225?auto=format&fit=crop&w=500&q=60"}
        ]
    },
    {
        "nombre": "Green Life 🥗",
        "descripcion": "Comida saludable, ensaladas y batidos.",
        "ubicacion": "Castillogrande",
        "imagen_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=800&q=80",
        "productos": [
            {"nombre": "Ensalada César", "precio": 18000, "descripcion": "Lechuga, pollo, crutones y parmesano.", "imagen_url": "https://images.unsplash.com/photo-1550304943-4f24f54ddde9?auto=format&fit=crop&w=500&q=60"},
            {"nombre": "Bowl de Quinoa", "precio": 24000, "descripcion": "Quinoa, aguacate, tomate y huevo.", "imagen_url": "https://images.unsplash.com/photo-1543339308-43e59d6b73a6?auto=format&fit=crop&w=500&q=60"},
            {"nombre": "Smoothie Verde", "precio": 10000, "descripcion": "Espinaca, manzana y piña.", "imagen_url": "https://images.unsplash.com/photo-1610970881699-44a5587cabec?auto=format&fit=crop&w=500&q=60"}
        ]
    }
]

def seed_db():
    db = SessionLocal()
    try:
        print("🌱 Iniciando sembrado de datos...")
        
        # Opcional: Limpiar tablas existentes (descomentar si quieres borrar todo antes)
        # db.query(Product).delete()
        # db.query(Kitchen).delete()
        # db.commit()

        for cocina_info in cocinas_data:
            # Separamos los productos de la info de la cocina
            productos_data = cocina_info.pop("productos")
            
            # Crear cocina
            cocina = Kitchen(**cocina_info)
            db.add(cocina)
            db.commit()
            db.refresh(cocina)
            
            print(f"✅ Cocina creada: {cocina.nombre}")

            # Crear productos para esa cocina
            for prod in productos_data:
                producto = Product(**prod, cocina_id=cocina.id, disponible=True)
                db.add(producto)
            
            db.commit()
            print(f"   --> {len(productos_data)} productos agregados.")

        print("🚀 ¡Base de datos poblada con éxito!")

    except Exception as e:
        print(f"❌ Error al poblar datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()