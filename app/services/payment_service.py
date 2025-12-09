import uuid
import time
import random

def procesar_pago_simulado(monto: float, datos_tarjeta: dict = None):
    """
    Simula una llamada a una API externa como Stripe o Wompi.
    Retorna un ID de transacción si es exitoso, o lanza error si falla.
    """
    print(f"🔄 Conectando con Pasarela de Pagos... Monto: ${monto}")
    
    # 1. Simular latencia de red (el tiempo que tarda el banco en responder)
    time.sleep(2) 
    
    # 2. Simular probabilidad de fallo (Opcional: aquí asumimos éxito siempre)
    # Si quisieras probar fallos, podrías descomentar esto:
    # if random.choice([True, False]): 
    #     raise Exception("Fondos insuficientes o tarjeta rechazada")
    
    # 3. Generar un ID de transacción falso (como lo haría un banco)
    transaction_id = f"TX-{uuid.uuid4().hex[:10].upper()}"
    
    print(f"✅ Pago Aprobado. ID Transacción: {transaction_id}")
    return transaction_id