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
            "imagen": "https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?q=80&w=1115&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            "descripcion": "Las mejores hamburguesas a la parrilla.",
            "ubicacion": "Bocagrande, Carrera 3",
            "menu": [
                {
                    "nombre": "Ghost Classic", 
                    "precio": 22000, 
                    "desc": "Carne 180g, queso cheddar, tocineta.", 
                    # Foto: Hamburguesa clásica
                    "imagen_producto": "https://plus.unsplash.com/premium_photo-1675252369719-dd52bc69c3df?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                },
                {
                    "nombre": "Doble Muerte", 
                    "precio": 32000, 
                    "desc": "Doble carne, doble queso, aros de cebolla.", 
                    # Foto: Hamburguesa doble
                    "imagen_producto": "https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?q=80&w=1115&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                },
                {
                    "nombre": "Papas Fantasma", 
                    "precio": 12000, 
                    "desc": "Papas rústicas con paprika.", 
                    # Foto: Papas fritas
                    "imagen_producto": "https://images.unsplash.com/photo-1762284513031-3d7ad15562bc?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                },
                {
                    "nombre": "Coca Cola Personal", 
                    "precio": 5000, 
                    "desc": "Botella 400ml fría.", 
                    # Foto: Refresco
                    "imagen_producto": "https://supermercadocomunal.com/verbenal/514-large_default/gaseosa-coca-cola-400-ml.jpg"
                },
                {
                    "nombre": "Coca Cola 2 Litros", 
                    "precio": 10000, 
                    "desc": "Botella 400ml fría.", 
                    # Foto: Refresco
                    "imagen_producto": "https://www.merkadomi.com/wp-content/uploads/2018/07/COCA-COLA-ORIGINAL-RETORNABLE-2L.jpg"
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
                    "imagen_producto": "https://images.unsplash.com/photo-1708782281073-1398b60158a7?q=80&w=880&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                },
                {
                    "nombre": "Carbonara", 
                    "precio": 32000, 
                    "desc": "Jamón y piña calada.", 
                    "imagen_producto": "https://plus.unsplash.com/premium_photo-1661762555601-47d088a26b50?q=80&w=1192&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                },
                {
                    "nombre": "Coca Cola Personal", 
                    "precio": 5000, 
                    "desc": "Botella 400ml fría.", 
                    # Foto: Refresco
                    "imagen_producto": "https://supermercadocomunal.com/verbenal/514-large_default/gaseosa-coca-cola-400-ml.jpg"
                },
                {
                    "nombre": "Coca Cola 2 Litros", 
                    "precio": 10000, 
                    "desc": "Botella 400ml fría.", 
                    # Foto: Refresco
                    "imagen_producto": "https://www.merkadomi.com/wp-content/uploads/2018/07/COCA-COLA-ORIGINAL-RETORNABLE-2L.jpg"
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
                },
                {
                    "nombre": "Coca Cola Personal", 
                    "precio": 5000, 
                    "desc": "Botella 400ml fría.", 
                    # Foto: Refresco
                    "imagen_producto": "https://supermercadocomunal.com/verbenal/514-large_default/gaseosa-coca-cola-400-ml.jpg"
                },
                {
                    "nombre": "Coca Cola 2 Litros", 
                    "precio": 10000, 
                    "desc": "Botella 400ml fría.", 
                    # Foto: Refresco
                    "imagen_producto": "https://www.merkadomi.com/wp-content/uploads/2018/07/COCA-COLA-ORIGINAL-RETORNABLE-2L.jpg"
                }
            ]
        },
        {
            "nombre": "Pollos Hermanos 🍗",
            # Foto portada: Pollo frito
            "imagen": "https://images.unsplash.com/photo-1562967916-eb82221dfb92?q=80&w=686&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            "descripcion": "Especialistas en pollo frito crujiente y acompañamientos.",
            "ubicacion": "Manga",
            "menu": [
                {
                    "nombre": "Pollo Frito Clásico",
                    "precio": 22000,
                    "desc": "Piezas de pollo frito crujiente con especias.",
                    "imagen_producto": "https://images.unsplash.com/photo-1562967916-eb82221dfb92?q=80&w=686&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                },
                {
                    "nombre": "Alitas BBQ",
                    "precio": 18000,
                    "desc": "Alitas bañadas en salsa BBQ ahumada.",
                    "imagen_producto": "https://plus.unsplash.com/premium_photo-1669742928112-19364a33b530?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                },
                {
                    "nombre": "Hamburguesa de Pollo Crispy",
                    "precio": 20000,
                    "desc": "Filete de pollo empanizado con lechuga y mayonesa.",
                    "imagen_producto": "https://images.unsplash.com/photo-1615297928064-24977384d0da?q=80&w=1112&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                },
                {
                    "nombre": "Papas Fritas",
                    "precio": 12000,
                    "desc": "Porción de papas fritas crujientes.",
                    "imagen_producto": "https://images.unsplash.com/photo-1630431341973-02e1b662ec35?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                },
                {
                    "nombre": "Coca Cola Personal", 
                    "precio": 5000, 
                    "desc": "Botella 400ml fría.", 
                    # Foto: Refresco
                    "imagen_producto": "https://supermercadocomunal.com/verbenal/514-large_default/gaseosa-coca-cola-400-ml.jpg"
                },
                {
                    "nombre": "Coca Cola 2 Litros", 
                    "precio": 10000, 
                    "desc": "Botella 400ml fría.", 
                    # Foto: Refresco
                    "imagen_producto": "https://www.merkadomi.com/wp-content/uploads/2018/07/COCA-COLA-ORIGINAL-RETORNABLE-2L.jpg"
                }
            ]
        },
        {
            "nombre": "El Gran Taco Fiesta 🌮",
            # Foto portada: Tacos mexicanos
            "imagen": "https://images.unsplash.com/photo-1613409385222-3d0decb6742a?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            "descripcion": "Auténtica comida mexicana con sazón tradicional.",
            "ubicacion": "Manga",
            "menu": [
                {
                    "nombre": "Tacos al Pastor",
                    "precio": 18000,
                    "desc": "Tortillas de maíz con cerdo adobado y piña.",
                    "imagen_producto": "https://images.unsplash.com/photo-1613409385222-3d0decb6742a?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                },
                {
                    "nombre": "Quesadilla de Pollo",
                    "precio": 16000,
                    "desc": "Tortilla rellena de queso derretido y pollo sazonado.",
                    "imagen_producto": "https://images.unsplash.com/photo-1618040996337-56904b7850b9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                },
                {
                    "nombre": "Burrito Especial",
                    "precio": 22000,
                    "desc": "Relleno de carne, arroz, frijoles y guacamole.",
                    "imagen_producto": "https://images.unsplash.com/photo-1731090389603-d63060ee08a6?q=80&w=1169&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                },
                {
                    "nombre": "Nachos con Queso",
                    "precio": 15000,
                    "desc": "Totopos crujientes con queso cheddar y jalapeños.",
                    "imagen_producto": "https://images.unsplash.com/photo-1572680443530-225d4e0d9894?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                },
                {
                    "nombre": "Coca Cola Personal", 
                    "precio": 5000, 
                    "desc": "Botella 400ml fría.", 
                    # Foto: Refresco
                    "imagen_producto": "https://supermercadocomunal.com/verbenal/514-large_default/gaseosa-coca-cola-400-ml.jpg"
                },
                {
                    "nombre": "Coca Cola 2 Litros", 
                    "precio": 10000, 
                    "desc": "Botella 400ml fría.", 
                    # Foto: Refresco
                    "imagen_producto": "https://www.merkadomi.com/wp-content/uploads/2018/07/COCA-COLA-ORIGINAL-RETORNABLE-2L.jpg"
                }
            ]
        },
        {
            "nombre": "El Dragón Oriental 🐲",
            "imagen": "https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=800&q=80",
            "descripcion": "Auténtica comida china con recetas tradicionales.",
            "ubicacion": "San Fernando",
            "menu": [
                {
                    "nombre": "Caja de Arroz Frito Especial",
                    "precio": 30000,
                    "desc": "Arroz frito con pollo, camarón, huevo y vegetales.",
                    "imagen_producto": "https://img0.didiglobal.com/static/soda_public/img_f3e44e340bff09b08b4c16a87a728de2.jpg"
                },
                {
                    "nombre": "Ramen Oriental",
                    "precio": 25000,
                    "desc": "Caldo intenso con fideos, cerdo y huevo cocido.",
                    "imagen_producto": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=500&q=60"
                },
                {
                    "nombre": "Pollo Agridulce",
                    "precio": 28000,
                    "desc": "Crujiente pollo en salsa agridulce con piña.",
                    "imagen_producto": "https://plus.unsplash.com/premium_photo-1692835633672-50919fdffb75?q=80&w=688&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                },
                {
                    "nombre": "Chow Mein de Pollo",
                    "precio": 27000,
                    "desc": "Fideos salteados con verduras y salsa de soya.",
                    "imagen_producto": "https://images.unsplash.com/photo-1609183480237-ccbb2d7c5772?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                },
                {
                    "nombre": "Coca Cola Personal", 
                    "precio": 5000, 
                    "desc": "Botella 400ml fría.", 
                    # Foto: Refresco
                    "imagen_producto": "https://supermercadocomunal.com/verbenal/514-large_default/gaseosa-coca-cola-400-ml.jpg"
                },
                {
                    "nombre": "Coca Cola 2 Litros", 
                    "precio": 10000, 
                    "desc": "Botella 400ml fría.", 
                    # Foto: Refresco
                    "imagen_producto": "https://www.merkadomi.com/wp-content/uploads/2018/07/COCA-COLA-ORIGINAL-RETORNABLE-2L.jpg"
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