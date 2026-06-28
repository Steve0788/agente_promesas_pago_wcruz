# tools.py - Herramientas del agente

from datetime import datetime
from database import obtener_cliente, registrar_promesa, listar_clientes
from langchain.tools import tool

@tool
def consultar_cliente(nombre: str) -> str:
    """
    Consulta los datos de un cliente por su nombre.
    Devuelve: deuda total, días en mora, canal de contacto.
    """
    cliente = obtener_cliente(nombre)
    if not cliente:
        return f"No se encontró información del cliente '{nombre}'."
    
    return (
        f"Cliente: {nombre}\n"
        f"Deuda total: ${cliente['deuda']:.2f}\n"
        f"Días en mora: {cliente['dias_mora']}\n"
        f"Canal de contacto: {cliente['canal']}"
    )

@tool
def registrar_promesa(nombre_cliente: str, monto: float, fecha_compromiso: str) -> str:
    """
    Registra una promesa de pago para un cliente.
    Fecha debe estar en formato YYYY-MM-DD.
    """
    cliente = obtener_cliente(nombre_cliente)
    if not cliente:
        return f"No se encontró el cliente '{nombre_cliente}'."

    # Validar formato de fecha
    try:
        datetime.strptime(fecha_compromiso, "%Y-%m-%d")
    except ValueError:
        return "❌ Formato de fecha inválido. Usa YYYY-MM-DD."

    # Validar que el monto no supere la deuda total
    if monto > cliente["deuda"]:
        return f"❌ El monto ${monto:.2f} supera la deuda total de ${cliente['deuda']:.2f}."

    registrar_promesa(nombre_cliente, monto, fecha_compromiso)
    return f"✅ Promesa de pago registrada: ${monto:.2f} para el {fecha_compromiso}."

@tool
def listar_clientes_disponibles() -> str:
    """
    Devuelve la lista de nombres de clientes disponibles en la base de datos.
    """
    clientes = listar_clientes()
    return "Clientes disponibles:\n- " + "\n- ".join(clientes)

@tool
def analizar_sentimiento(mensaje: str) -> str:
    """
    Analiza el sentimiento de un mensaje del cliente.
    Devuelve: positivo, negativo, neutral, enojado.
    """
    mensaje_lower = mensaje.lower()
    
    # Palabras clave para detectar emociones
    negativo = ["queja", "mal", "pésimo", "decepcionado", "enojado", "molesto", "indignado", "inaceptable"]
    enojado = ["insulto", "estafa", "ladrón", "incompetente", "farsa", "baja"]
    positivo = ["gracias", "excelente", "bueno", "claro", "entendido", "perfecto", "acuerdo"]
    
    for palabra in enojado:
        if palabra in mensaje_lower:
            return "molesto"
    
    for palabra in negativo:
        if palabra in mensaje_lower:
            return "negativo"
    
    for palabra in positivo:
        if palabra in mensaje_lower:
            return "positivo"
    
    return "neutral"

@tool
def resumir_conversacion(mensajes: list) -> str:
    """
    Resumen breve de la conversación.
    """
    if not mensajes:
        return "No hay mensajes para resumir."
    
    total = len(mensajes)
    resumen = f"Conversación de {total} mensajes. "
    resumen += "Incluye interacción sobre negociación de pago."
    return resumen