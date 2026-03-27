import streamlit as st
import os
import sys

# Configuración de página
st.set_page_config(
    page_title="RAG DOCS",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS INYECTADO: ELIMINACIÓN DE AZULES Y GRISES ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Inter:wght@400;500&display=swap');

    /* Fondo base y tipografía */
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { 
        background-color: #050505; 
        color: #FFFFFF;
    }

    /* FORZAR COLOR EN EL INPUT DE CHAT (Elimina el azul/gris por defecto) */
    .stChatInput > div {
        background: rgba(25, 25, 25, 0.4) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(229, 62, 62, 0.2) !important; /* Borde carmesí sutil */
        border-radius: 15px !important;
    }
    
    .stChatInput textarea {
        color: #FFFFFF !important;
    }

    /* Botón de enviar: Rojo Carmesí */
    .stChatInput button {
        background-color: #E53E3E !important;
        color: white !important;
    }

    /* Sidebar Crystal */
    section[data-testid="stSidebar"] {
        background: rgba(15, 15, 15, 0.7) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }

    /* Botones del sistema */
    .stButton > button {
        background: rgba(40, 40, 40, 0.5) !important;
        color: white !important;
        border: 1px solid rgba(229, 62, 62, 0.3) !important;
        border-radius: 10px !important;
    }
    .stButton > button:hover {
        background: #E53E3E !important;
        border-color: #E53E3E !important;
    }

    /* Header e Iconos */
    .fitcoach-header {
        display: flex; align-items: center; gap: 15px;
        padding: 20px; background: rgba(20, 20, 20, 0.5);
        border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .fitcoach-logo {
        background: linear-gradient(135deg, #E53E3E, #9B1C1C);
        padding: 15px; border-radius: 12px;
    }
    
    /* Fix para el menú de hamburguesa */
    header[data-testid="stHeader"] {
        background: transparent !important;
        color: #E53E3E !important;
    }
    #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Lógica de persistencia
if "messages" not in st.session_state: st.session_state.messages = []
if "initialized" not in st.session_state: st.session_state.initialized = False

# Sidebar
with st.sidebar:
    st.markdown("<h2 style='color:#E53E3E;'>RAG DOCS</h2>", unsafe_allow_html=True)
    st.text_input("Directorio de documentos", value="C:\\Users\\Bryan\\Documentos") # Basado en tu estructura
    if st.button("CARGAR 📥", use_container_width=True):
        st.session_state.initialized = True
        st.success("Documentos cargados")

# Contenedor Principal
st.markdown("""
<div class="fitcoach-header">
    <div class="fitcoach-logo">🤖</div>
    <div>
        <h2 style="margin:0;">RAG<span style="color:#E53E3E;">DOCS</span></h2>
        <small style="color:#888;">Interfaz Protegida | Estudiante de Software</small>
    </div>
</div>
""", unsafe_allow_html=True)

# Historial
for msg in st.session_state.messages:
    color = "rgba(229, 62, 62, 0.2)" if msg["role"] == "user" else "rgba(30, 30, 30, 0.6)"
    st.markdown(f"<div style='background:{color}; padding:15px; border-radius:12px; margin-bottom:10px;'>{msg['content']}</div>", unsafe_allow_html=True)

# Chat Input
if prompt := st.chat_input("¿Qué deseas consultar de tus archivos?", disabled=not st.session_state.initialized):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": "Analizando contexto..."})
    st.rerun()