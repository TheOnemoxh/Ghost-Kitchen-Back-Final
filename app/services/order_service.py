from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException

# Modelos
from app.models.order import Order, OrderDetail, OrderStatus
from app.models.product import Product
# Importamos Address desde user.py para la validación
from app.models.user import Address 

# Schemas
from app.schemas.order import OrderCreate

# Servicios externos
from app.services.payment_service import procesar_pago_simulado 

# ---------------------------------------------------------
# 1. CREAR PEDIDO
# ---------------------------------------------------------
def crear_pedido(db: Session, order_data: OrderCreate, user_id: int):
    total_calculado = 0.0
    items_procesados = []
    
    # 0. VALIDACIÓN DE DIRECCIÓN (Seguridad)
    # Verificamos que la dirección exista Y pertenezca al usuario que está comprando
    direccion = db.query(Address).filter(
        Address.id == order_data.direccion_id, 
        Address.usuario_id == user_id
    ).first()
    
    if not direccion:
        raise HTTPException(
            status_code=400, 
            detail="La dirección seleccionada no es válida o no pertenece al usuario"
        )

    # 1. Validar productos y calcular total
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

    # 2. Procesar pago si es necesario
    id_transaccion = None
    
    if order_data.metodo_pago == "LINEA":
        try:
            id_transaccion = procesar_pago_simulado(total_calculado)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error pago: {str(e)}")

    # 3. Crear el Pedido en BD
    nuevo_pedido = Order(
        cliente_id=user_id,
        direccion_id=order_data.direccion_id, # 👈 AQUÍ SE GUARDA LA DIRECCIÓN
        estado=OrderStatus.CONFIRMED.value,
        total=total_calculado,
        metodo_pago=order_data.metodo_pago,
        id_transaccion=id_transaccion
    )
    
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)
    
    # 4. Guardar los detalles
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
# 2. CANCELAR PEDIDO
# ---------------------------------------------------------
def cancelar_pedido(db: Session, order_id: int, user_id: int):
    order = db.query(Order).filter(
        Order.id == order_id, 
        Order.cliente_id == user_id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    if order.estado != OrderStatus.CONFIRMED.value:
        raise HTTPException(
            status_code=400, 
            detail="El pedido ya está en preparación o camino y no puede ser cancelado."
        )

    order.estado = OrderStatus.CANCELLED.value
    db.commit()
    db.refresh(order)
    
    return {"mensaje": "Pedido cancelado exitosamente", "estado": order.estado}


# ---------------------------------------------------------
# 3. OBTENER HISTORIAL
# ---------------------------------------------------------
def obtener_historial_cliente(db: Session, user_id: int):
    ordenes = db.query(Order)\
             .filter(Order.cliente_id == user_id)\
             .order_by(Order.fecha.desc())\
             .all()
    
    resultado = []
    for o in ordenes:
        resultado.append({
            "id": o.id,
            "fecha": o.fecha,
            "total": float(o.total),
            "estado": str(o.estado),
            "metodo_pago": str(o.metodo_pago),
            "cantidad_items": len(o.detalles)
        })
        
    return resultado


# ---------------------------------------------------------
# 4. OBTENER DETALLE
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

    return {
        "id": order.id,
        "fecha": order.fecha,
        "estado": str(order.estado),
        "total": float(order.total),
        "metodo_pago": str(order.metodo_pago),
        "id_transaccion": order.id_transaccion,
        "items": items_formateados
    }


# ---------------------------------------------------------
# 5. OBTENER ÚLTIMO PEDIDO ACTIVO
# ---------------------------------------------------------
def obtener_ultimo_pedido_activo(db: Session, user_id: int):
    pedido_activo = db.query(Order).filter(
        Order.cliente_id == user_id,
        Order.estado.notin_([OrderStatus.DELIVERED.value, OrderStatus.CANCELLED.value])
    ).order_by(desc(Order.fecha)).first()

    if not pedido_activo:
        return None

    return {"id": pedido_activo.id}