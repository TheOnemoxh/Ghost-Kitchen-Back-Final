from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.order import Order, OrderDetail
from app.models.product import Product
from app.schemas.order import OrderCreate
# Importamos la simulación de pago
from app.services.payment_service import procesar_pago_simulado 

# ---------------------------------------------------------
# 1. CREAR PEDIDO
# ---------------------------------------------------------
def crear_pedido(db: Session, order_data: OrderCreate, user_id: int):
    total_calculado = 0.0
    items_procesados = []
    
    for item in order_data.items:
        producto = db.query(Product).filter(Product.id == item.producto_id).first()
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto ID {item.producto_id} no encontrado")
        
        subtotal = producto.precio * item.cantidad
        total_calculado += subtotal
        
        items_procesados.append({
            "producto_id": producto.id,
            "cantidad": item.cantidad,
            "precio_unitario": producto.precio
        })

    estado_inicial = "CONFIRMADO"
    id_transaccion = None
    
    if order_data.metodo_pago == "LINEA":
        try:
            id_transaccion = procesar_pago_simulado(total_calculado)
            estado_inicial = "PAGADO"
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error pago: {str(e)}")

    nuevo_pedido = Order(
        cliente_id=user_id, 
        estado=estado_inicial, 
        total=total_calculado,
        metodo_pago=order_data.metodo_pago,
        id_transaccion=id_transaccion
    )
    
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)
    
    for item_data in items_procesados:
        detalle = OrderDetail(
            pedido_id=nuevo_pedido.id,
            producto_id=item_data["producto_id"],
            cantidad=item_data["cantidad"],
            precio_unitario=item_data["precio_unitario"]
        )
        db.add(detalle)
    
    db.commit()
    return nuevo_pedido


# ---------------------------------------------------------
# 2. OBTENER HISTORIAL (CORREGIDO - MANUAL)
# ---------------------------------------------------------
def obtener_historial_cliente(db: Session, user_id: int):
    # Obtenemos los objetos de la BD
    ordenes = db.query(Order)\
             .filter(Order.cliente_id == user_id)\
             .order_by(Order.fecha.desc())\
             .all()
    
    # 🔥 SOLUCIÓN DEFINITIVA: Convertimos a diccionarios manualmente
    # Esto evita que Pydantic intente leer atributos lazy que fallan
    resultado = []
    for o in ordenes:
        resultado.append({
            "id": o.id,
            "fecha": o.fecha,
            "total": float(o.total), # Aseguramos float
            "estado": str(o.estado),
            "metodo_pago": str(o.metodo_pago),
            "cantidad_items": len(o.detalles) # Calculamos aquí
        })
        
    return resultado


# ---------------------------------------------------------
# 3. OBTENER DETALLE (CORREGIDO - MANUAL)
# ---------------------------------------------------------
def obtener_detalle_pedido(db: Session, order_id: int, user_id: int):
    order = db.query(Order).filter(
        Order.id == order_id, 
        Order.cliente_id == user_id
    ).first()
    
    if not order:
        return None

    items_formateados = []
    for detalle in order.detalles:
        items_formateados.append({
            "producto_nombre": detalle.producto.nombre,
            "cantidad": detalle.cantidad,
            "precio_unitario": float(detalle.precio_unitario),
            "subtotal": float(detalle.precio_unitario * detalle.cantidad),
            "imagen_producto": detalle.producto.descripcion 
        })

    # Retornamos diccionario puro
    return {
        "id": order.id,
        "fecha": order.fecha,
        "estado": str(order.estado),
        "total": float(order.total),
        "metodo_pago": str(order.metodo_pago),
        "id_transaccion": order.id_transaccion,
        "items": items_formateados
    }