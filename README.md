# 🤖 Agente Inteligente de Promesas de Pago

**Semillero de IA**

## 📌 Descripción del proyecto

Este proyecto implementa un agente conversacional autónomo que automatiza la negociación y el registro de **promesas de pago** con clientes morosos. El agente utiliza un modelo de lenguaje (LLM) y herramientas personalizadas para:

1.  **Validar la cartera del cliente**.
2.  **Negociar** un acuerdo de pago personalizado.
3.  **Identificar** la fecha de compromiso.
4.  **Registrar** la promesa de pago y generar un resumen.

Este proyecto fue desarrollado como entrega final para el Semillero de Inteligencia Artificial, aplicando todos los conceptos aprendidos sobre agentes, herramientas (tools), observabilidad, evaluación y seguridad.

---

## 🛠️ Tecnologías y herramientas utilizadas

- **Python 3.11**: Lenguaje de programación principal.
- **Ollama**: Para ejecutar modelos de lenguaje localmente o en la nube (Gemma 4).
- **LangChain & LangGraph**: Framework para la creación y orquestación del agente.
- **Gradio**: Para construir la interfaz gráfica de usuario (UI) de manera sencilla e interactiva.
- **Pandas**: Para el manejo y visualización de datos simulados.

---

## ⚙️ Instalación y configuración

Pasos para ejecutar el proyecto.

1. Clonar el repositorio
```bash
git clone [http://127.0.0.1:7860/]
cd agente_promesas_pago_wcruz


2. Crear y activar un entorno virtual 
python -m venv venv
venv\Scripts\activate

3. Instalar las dependencias
pip install -r requirements.txt

4. Configurar el modelo (Ollama)
Asegúrate de tener Ollama instalado y ejecutándose. Puedes usar el modelo por defecto (gemma4:31b-cloud) o cambiarlo en el archivo app.py. Para verificar que el modelo esté disponible, ejecuta en tu terminal:

ollama list
Si no lo tienes, descárgalo con:

ollama pull gemma4:31b-cloud
🚀 Ejecución
Para iniciar la aplicación, ejecuta el siguiente comando en la raíz del proyecto:

python app.py
La interfaz gráfica de Gradio se abrirá automáticamente en tu navegador en la dirección http://127.0.0.1:7860.

🧪 Datos de ejemplo
El sistema incluye datos simulados para pruebas, con clientes (nombres de héroes de Dota 2) que tienen distintos montos de deuda y días de mora:

Axe · $250.00 · 30 días · WhatsApp

Juggernaut · $120.50 · 15 días · Email

Crystal Maiden · $45.20 · 5 días · WhatsApp

Pudge · $500.00 · 60 días · Llamada

Phantom Assassin · $780.30 · 45 días · WhatsApp

Invoker · $320.00 · 20 días · Email

🛠️ Herramientas del agente
El agente cuenta con 5 herramientas que le permiten operar de forma autónoma:

Herramienta	Descripción
consultar_cliente	Obtiene la deuda y días de mora de un cliente.
registrar_promesa	Almacena una promesa de pago (monto y fecha) en el sistema.
listar_clientes_disponibles	Muestra todos los clientes disponibles para la negociación.
analizar_sentimiento	Detecta el estado emocional del cliente (positivo, negativo, enojado, neutral).
resumir_conversacion	Genera un resumen de toda la interacción con el cliente.

🧠 Diagrama del agente
A continuación, se muestra un diagrama simplificado del flujo de trabajo del agente:


[Usuario escribe su mensaje]
         │
         ▼
[Agente recibe el mensaje + contexto del cliente]
         │
         ▼
[El agente procesa la solicitud con el LLM (Gemma 4)]
         │
         ▼
┌─────────────────────────────────┐
│ El agente decide si necesita   │
│ usar alguna herramienta.       │
└─────────────────────────────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
[Herramienta] [Respuesta Directa]
    │              │
    ▼              │
[Observa el       │
 resultado]       │
    │              │
    └──────┬───────┘
           ▼
[Genera una respuesta final y la envía al chat]
           │
           ▼
[La interfaz Gradio muestra la respuesta al usuario]

🎯 Ejemplos de conversación
1. Negociación exitosa
Usuario (cliente: Axe): "Hola, quiero pagar mi deuda."
Agente: "¡Hola Axe! Soy el Asistente de Promesas de Pago. Actualmente tienes una deuda de $250.00 con 30 días de mora. ¿Qué opción te acomoda mejor? ..."

2. Cliente enojado
Usuario (cliente: Pudge): "Esto es un abuso y una estafa, no pienso pagar."
Agente: "Comprendo tu molestia, Pudge. Entiendo que esta situación es frustrante. Sin embargo, es importante encontrar una solución. ..."

📦 Estructura del proyecto
agente_promesas_pago_wcruz/
├── .gitignore              # Archivos y carpetas ignorados por Git
├── .env.example            # Variables de entorno de ejemplo
├── app.py                  # Código principal de la aplicación y la interfaz
├── database.py             # Datos simulados de los clientes
├── prompts.py              # System prompt y mensajes predefinidos
├── requirements.txt        # Dependencias del proyecto
├── tools.py                # Herramientas personalizadas del agente
└── README.md               # Este archivo, documentación del proyecto

👨‍💻 Desarrollador
Steve– Steve0788

📚 Agradecimientos
#Este proyecto fue desarrollado como parte del Semillero de Inteligencia Artificial, aplicando todas las lecciones y herramientas aprendidas durante el curso.

Los nombres de los clientes son homenaje a los héroes del videojuego Dota 2.

