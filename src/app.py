# -*- coding: utf-8 -*-
"""
Interfaz web del Agente Modova, construida con Streamlit.
Permite a cualquier usuario hacer preguntas en lenguaje natural sobre
las políticas de Modova (privacidad, reembolsos, envíos, FAQ, términos).
"""

import streamlit as st

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.agent import AgenteModova

st.set_page_config(
    page_title="Agente Modova",
    page_icon="🛍️",
    layout="centered",
)

# --- Estilos mínimos ---
st.markdown(
    """
    <style>
    .stChatMessage { font-size: 16px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Cabecera ---
st.title("🛍️ Agente Modova")
st.caption(
    "Asistente virtual de Modova — pregunta sobre envíos, devoluciones, "
    "privacidad, pagos y más. Basado en la documentación oficial de la tienda."
)


@st.cache_resource(show_spinner="Cargando el agente por primera vez... esto puede tardar un momento ⏳")
def cargar_agente():
    """Inicializa el agente una sola vez y lo mantiene en caché entre interacciones."""
    return AgenteModova()


# --- Inicialización del agente (con manejo de errores de configuración) ---
try:
    agente = cargar_agente()
except EnvironmentError as e:
    st.error(f"⚠️ Error de configuración: {e}")
    st.stop()
except Exception as e:
    st.error(f"⚠️ No se pudo inicializar el agente: {e}")
    st.stop()

# --- Preguntas de ejemplo (sidebar) ---
with st.sidebar:
    st.header("💡 Preguntas de ejemplo")
    ejemplos = [
        "¿Cuántos días tengo para devolver un producto?",
        "¿Hacen envíos gratis?",
        "¿Qué pasa si mi pedido llega dañado?",
        "¿Tienen tienda física?",
        "¿Cómo funciona el programa Modova Club?",
        "¿Qué métodos de pago aceptan?",
    ]
    for ejemplo in ejemplos:
        if st.button(ejemplo, use_container_width=True):
            st.session_state["pregunta_sugerida"] = ejemplo

# --- Historial del chat ---
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {
            "role": "assistant",
            "content": "¡Hola! 👋 Soy el asistente virtual de Modova. "
                       "¿En qué puedo ayudarte hoy?",
        }
    ]

for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# --- Entrada del usuario ---
pregunta_sugerida = st.session_state.pop("pregunta_sugerida", None)
pregunta = st.chat_input("Escribe tu pregunta...") or pregunta_sugerida

if pregunta:
    st.session_state.mensajes.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            respuesta = agente.preguntar(pregunta)
            st.markdown(respuesta)

    st.session_state.mensajes.append({"role": "assistant", "content": respuesta})