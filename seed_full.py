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
        # Borramos primero productos (por la llave foránea) y luego cocinas
        db.query(Product).delete()
        db.query(Kitchen).delete()
        db.commit()
    except Exception as e:
        print(f"Nota: No se pudo limpiar o estaba vacía ({e})")
        db.rollback()

    print("🌱 Creando 6 Cocinas y sus Menús...")

    # --- DEFINICIÓN DE DATOS ---
    
    cocinas_data = [
        {
            "nombre": "Ghost Burger 👻",
            "imagen": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80",
            "descripcion": "Las mejores hamburguesas a la parrilla.",
            "ubicacion": "Bocagrande, Carrera 3",
            "menu": [
                {"nombre": "Ghost Classic", "precio": 22000, "desc": "Carne 180g, queso cheddar, tocineta y salsa secreta."},
                {"nombre": "Doble Muerte", "precio": 32000, "desc": "Doble carne, doble queso, aros de cebolla."},
                {"nombre": "Papas Fantasma", "precio": 12000, "desc": "Papas rústicas con paprika y queso fundido."},
                {"nombre": "Coca Cola Zero", "precio": 5000, "desc": "Lata 330ml fría."}
            ]
        },
        {
            "nombre": "Pizza Planet 🍕",
            "imagen": "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=80",
            "descripcion": "Masa madre y horno de leña.",
            "ubicacion": "Centro Histórico",
            "menu": [
                {"nombre": "Pepperoni Lover", "precio": 35000, "desc": "Extra pepperoni, queso mozzarella y orégano."},
                {"nombre": "Hawaiana", "precio": 32000, "desc": "Jamón, piña calada y extra queso."},
                {"nombre": "Margarita", "precio": 28000, "desc": "Tomate, albahaca fresca y mozzarella de búfala."},
                {"nombre": "Cerveza Club", "precio": 8000, "desc": "Lata fría."}
            ]
        },
        {
            "nombre": "Sushi Master 🍣",
            "imagen": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&w=800&q=80",
            "descripcion": "Auténtica comida japonesa y fusión.",
            "ubicacion": "Manga, Avenida del Lago",
            "menu": [
                {"nombre": "Philadelphia Roll", "precio": 28000, "desc": "Salmón fresco, queso crema y ajonjolí (10 bocados)."},
                {"nombre": "Ojo de Tigre", "precio": 30000, "desc": "Tempura, palmito, salmón y salsa anguila."},
                {"nombre": "Ramen de Cerdo", "precio": 25000, "desc": "Caldo tradicional, huevo, cerdo y fideos."},
                {"nombre": "Limonada de Coco", "precio": 12000, "desc": "Natural y cremosa."}
            ]
        },
        {
            "nombre": "El Pollo Hermanos 🍗",
            "imagen": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?auto=format&fit=crop&w=800&q=80",
            "descripcion": "Pollo frito crujiente estilo americano.",
            "ubicacion": "Pie de la Popa",
            "menu": [
                {"nombre": "Combo Personal", "precio": 18000, "desc": "2 presas, papas fritas y gaseosa."},
                {"nombre": "Balde Familiar", "precio": 65000, "desc": "10 presas, 4 papas, ensalada y gaseosa 1.5L."},
                {"nombre": "Popcorn Chicken", "precio": 15000, "desc": "Trozos de pechuga apanada con salsa BBQ."},
                {"nombre": "Mazorca Dulce", "precio": 6000, "desc": "Con mantequilla y sal."}
            ]
        },
        {
            "nombre": "Taco Fiesta 🌮",
            "imagen": "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?auto=format&fit=crop&w=800&q=80",
            "descripcion": "Sabores de México en tu casa.",
            "ubicacion": "Getsemaní",
            "menu": [
                {"nombre": "Tacos al Pastor", "precio": 15000, "desc": "3 tacos de cerdo marinado con piña y cilantro."},
                {"nombre": "Burrito Gigante", "precio": 24000, "desc": "Arroz, frijol, carne desmechada, queso y guacamole."},
                {"nombre": "Nachos Supremos", "precio": 28000, "desc": "Para compartir. Con queso, pico de gallo y jalapeños."},
                {"nombre": "Agua de Jamaica", "precio": 5000, "desc": "Bebida refrescante natural."}
            ]
        },
        {
            "nombre": "Green Life 🥗",
            "imagen": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=800&q=80",
            "descripcion": "Comida saludable, bowls y ensaladas.",
            "ubicacion": "Castillogrande",
            "menu": [
                {"nombre": "Cesar Salad", "precio": 22000, "desc": "Lechuga romana, crutones, parmesano y pollo grillé."},
                {"nombre": "Poke Bowl Atún", "precio": 32000, "desc": "Arroz sushi, atún fresco, mango, aguacate y edamame."},
                {"nombre": "Wrap de Pavo", "precio": 18000, "desc": "Tortilla integral, jamón de pavo y vegetales."},
                {"nombre": "Smoothie Verde", "precio": 10000, "desc": "Espinaca, piña, pepino y manzana."}
            ]
        }
    ]

    # --- INSERCIÓN EN BD ---
    
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
        db.commit() # Guardar para obtener el ID
        db.refresh(nueva_cocina)
        
        print(f"🍳 Cocina creada: {nueva_cocina.nombre}")

        # 2. Crear Productos de esa cocina
        for p_data in k_data["menu"]:
            nuevo_producto = Product(
                nombre=p_data["nombre"],
                precio=p_data["precio"],
                descripcion=p_data["desc"],
                disponible=True,
                cocina_id=nueva_cocina.id
            )
            db.add(nuevo_producto)
        
        db.commit() # Guardar todos los productos de esta cocina

    print("✅ ¡Base de datos poblada exitosamente con 6 cocinas!")
    db.close()

if __name__ == "__main__":
    seed_full_data()