# app.py - Agente Inteligente de Promesas de Pago

import gradio as gr
from langchain_ollama import ChatOllama
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import (
    consultar_cliente,
    registrar_promesa,
    listar_clientes_disponibles,
    analizar_sentimiento,
    resumir_conversacion
)
from prompts import SYSTEM_PROMPT, MENSAJE_NO_ACUERDO, MENSAJE_ACUERDO
from database import obtener_cliente, listar_clientes

# Configurar el modelo
llm = ChatOllama(model="gemma4:31b-cloud", temperature=0.3)

# Definir herramientas del agente
tools = [
    consultar_cliente,
    registrar_promesa,
    listar_clientes_disponibles,
    analizar_sentimiento,
    resumir_conversacion
]

# Prompt del agente
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Crear el agente
agente = create_tool_calling_agent(llm, tools, prompt)

# Ejecutor del agente
ejecutor = AgentExecutor(
    agent=agente,
    tools=tools,
    max_iterations=10,
    handle_parsing_errors=True,
    verbose=False
)

# Historial de conversación por cliente
historiales = {}

def responder_mensaje(nombre_cliente, mensaje_usuario):
    """Procesa un mensaje del cliente y devuelve la respuesta del agente."""
    
    # Verificar si el cliente existe
    cliente = obtener_cliente(nombre_cliente)
    if not cliente:
        return f"❌ No se encontró al cliente '{nombre_cliente}'. Clientes disponibles: {', '.join(listar_clientes())}"
    
    # Inicializar historial si no existe
    if nombre_cliente not in historiales:
        historiales[nombre_cliente] = []
    
    # 🔥 CAMBIO IMPORTANTE: Incluir el nombre del cliente en el contexto
    contexto_inicial = f"El cliente es {nombre_cliente}. Su deuda es de ${cliente['deuda']:.2f} y tiene {cliente['dias_mora']} días de mora."
    
    # Construir contexto con historial (últimos 5 mensajes)
    contexto_historial = "\n".join(historiales[nombre_cliente][-5:])
    mensaje_completo = f"{contexto_inicial}\n{contexto_historial}\nCliente: {mensaje_usuario}".strip()
    
    try:
        # Ejecutar el agente
        resultado = ejecutor.invoke({"input": mensaje_completo})
        respuesta = resultado["output"]
        
        # Guardar en historial
        historiales[nombre_cliente].append(f"Usuario: {mensaje_usuario}")
        historiales[nombre_cliente].append(f"Asistente: {respuesta}")
        
        # Mantener historial acotado
        if len(historiales[nombre_cliente]) > 20:
            historiales[nombre_cliente] = historiales[nombre_cliente][-20:]
        
        return respuesta
    
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def resumen_conversacion_ui(nombre_cliente):
    """Genera resumen y análisis de sentimiento de la conversación."""
    if nombre_cliente not in historiales or not historiales[nombre_cliente]:
        return "No hay conversación registrada para este cliente."
    
    historial = historiales[nombre_cliente]
    texto_completo = " ".join(historial)
    
    sentimiento = analizar_sentimiento.invoke({"mensaje": texto_completo})
    resumen = resumir_conversacion.invoke({"mensajes": historial})
    
    return f"""
    📊 **Resumen de la conversación con {nombre_cliente}**
    
    {resumen}
    
    **Análisis de sentimiento:** {sentimiento}
    
    **Historial de mensajes:**
    {chr(10).join(f'- {msg}' for msg in historial)}
    """

# Interfaz con Gradio
with gr.Blocks(title="Agente de Promesas de Pago", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🤖 Agente Inteligente de Promesas de Pago")
    gr.Markdown("""
    El asistente negocia acuerdos de pago con clientes de manera **empática y profesional**.
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            cliente_dropdown = gr.Dropdown(
                choices=listar_clientes(),
                label="👤 Selecciona un cliente",
                value="Axe"
            )
            mensaje_input = gr.Textbox(
                label="💬 Escribe tu mensaje",
                placeholder="Ejemplo: Hola, quiero pagar mi deuda.",
                lines=3
            )
            enviar_btn = gr.Button("🚀 Enviar", variant="primary")
            limpiar_btn = gr.Button("🗑️ Limpiar historial", variant="secondary")
        
        with gr.Column(scale=2):
            respuesta_output = gr.Textbox(
                label="🤖 Respuesta del agente",
                lines=6,
                interactive=False
            )
            resumen_output = gr.Markdown(
                label="📝 Resumen de la conversación"
            )
    
    # Eventos
    enviar_btn.click(
        responder_mensaje,
        inputs=[cliente_dropdown, mensaje_input],
        outputs=respuesta_output
    ).then(
        lambda cliente: resumen_conversacion_ui(cliente),
        inputs=cliente_dropdown,
        outputs=resumen_output
    )
    
    cliente_dropdown.change(
        lambda cliente: resumen_conversacion_ui(cliente),
        inputs=cliente_dropdown,
        outputs=resumen_output
    )
    
    limpiar_btn.click(
        lambda cliente: historiales.__setitem__(cliente, []) or "Historial limpiado.",
        inputs=cliente_dropdown,
        outputs=respuesta_output
    ).then(
        lambda: "🔄 Historial reiniciado",
        outputs=resumen_output
    )

# Ejecutar la aplicación
if __name__ == "__main__":
    app.launch(share=False)