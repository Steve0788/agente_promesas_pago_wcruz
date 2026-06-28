# database.py - Datos simulados (nombres ficticios de Dota 2)

CLIENTES = {
    "Axe": {
        "deuda": 250.00,
        "dias_mora": 30,
        "canal": "WhatsApp",
        "email": "axe@dota2.com",
        "telefono": "0999123456"
    },
    "Juggernaut": {
        "deuda": 120.50,
        "dias_mora": 15,
        "canal": "Email",
        "email": "juggernaut@dota2.com",
        "telefono": "0999123457"
    },
    "Crystal Maiden": {
        "deuda": 45.20,
        "dias_mora": 5,
        "canal": "WhatsApp",
        "email": "crystal@dota2.com",
        "telefono": "0999123458"
    },
    "Pudge": {
        "deuda": 500.00,
        "dias_mora": 60,
        "canal": "Llamada",
        "email": "pudge@dota2.com",
        "telefono": "0999123459"
    },
    "Phantom Assassin": {
        "deuda": 780.30,
        "dias_mora": 45,
        "canal": "WhatsApp",
        "email": "pa@dota2.com",
        "telefono": "0999123460"
    },
    "Invoker": {
        "deuda": 320.00,
        "dias_mora": 20,
        "canal": "Email",
        "email": "invoker@dota2.com",
        "telefono": "0999123461"
    }
}

PROMESAS = {}

def obtener_cliente(nombre: str):
    """Obtiene los datos de un cliente por su nombre."""
    return CLIENTES.get(nombre, None)

def listar_clientes():
    """Devuelve la lista de nombres de clientes disponibles."""
    return list(CLIENTES.keys())

def registrar_promesa(cliente: str, monto: float, fecha_compromiso: str):
    """Registra una promesa de pago en el historial."""
    PROMESAS[cliente] = {
        "monto": monto,
        "fecha": fecha_compromiso
    }
    return True

def obtener_promesa(cliente: str):
    """Obtiene la promesa de pago de un cliente."""
    return PROMESAS.get(cliente, None)