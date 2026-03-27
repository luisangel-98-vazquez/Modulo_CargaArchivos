import streamlit as st
import os
import sys

# Configuración de página
st.set_page_config(
    page_title="Asistente IA",
    page_icon="🤖",
    layout="wide",
)

sys.path.append(os.path.dirname(__file__))
from RAGEngine import RAGEngine, DOCS_PATH, OLLAMA_MODEL

# ── CSS: FONDO TOTAL Y ESTILO DE BOTONES ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0b111e !important;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stMainViewContainer"] {
        background-color: #0b111e !important;
    }

    [data-testid="stMainViewContainer"] > section > div {
        padding-top: 2rem !important;
        padding-bottom: 0rem !important;
    }

    header[data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
        color: #3b82f6 !important;
    }
    #MainMenu, footer { visibility: hidden; }

    section[data-testid="stSidebar"] {
        background-color: #0e1626 !important;
        border-right: 1px solid #1e293b !important;
    }

    .main-card {
        background: rgba(17, 25, 40, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        max-width: 700px;
        margin: 20px auto;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    .stChatInput > div {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
    }

    .logo-box-blue {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        width: 45px; height: 45px; border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.3rem;
    }
</style>
""", unsafe_allow_html=True)

# ── LÓGICA DE SESIÓN ──
if "engine" not in st.session_state:
    st.session_state.engine = RAGEngine()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "initialized" not in st.session_state:
    st.session_state.initialized = False

# ── SIDEBAR CON BOTONES CARGAR Y LIMPIAR ──
with st.sidebar:
    st.markdown("""
    <div style='display:flex; align-items:center; gap:12px;'>
        <div class="logo-box-blue">👤</div>
        <h2 style='margin:0; font-size:1.2rem;'>Hola, <span style="color:#3b82f6;">Usuario</span> 👋</h2>
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    docs_path = st.text_input("Carpeta de documentos", value="C:\\Users\\luisa\\OneDrive\\Documentos")
    modelo = st.text_input("Modelo Ollama", value=OLLAMA_MODEL)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 CARGAR", use_container_width=True):
            st.session_state.engine.initialize(docs_path)
            st.session_state.initialized = True
            st.rerun()
    
    with col2:
        if st.button("🗑️ LIMPIAR", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

# ── CUERPO PRINCIPAL ──
st.markdown(f"""
<div style="display: flex; align-items: center; gap: 15px; margin-bottom: 5px;">
    <div class="logo-box-blue">🤖</div>
    <div>
        <h1 style="margin:0; font-size: 1.5rem; color: #3b82f6;">¿EN QUÉ TE PUEDO <span style="color:white;">AYUDAR HOY?</span></h1>
        <p style="margin:0; color: #64748b; font-size: 0.7rem; text-transform: uppercase;">Módulo de Consulta</p>
    </div>
</div>
<hr style="border: 0.5px solid #1e293b; margin-bottom: 15px;">
""", unsafe_allow_html=True)

if not st.session_state.initialized:
    st.markdown("""
    <div class="main-card">
        <div style="font-size: 3rem; margin-bottom: 10px;">📂</div>
        <h2 style="margin:0; font-size:1.6rem;">CARGA TUS DOCUMENTOS</h2>
        <p style="color:#64748b; margin-top:5px; font-size:0.9rem;">Configura la carpeta y presiona Cargar para comenzar.</p>
    </div>
    """, unsafe_allow_html=True)

# Renderizado de historial
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ── INPUT DE CHAT ──
prompt = st.chat_input("Pregunta sobre tus archivos...", disabled=not st.session_state.initialized)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    response = st.session_state.engine.query(prompt)
    
    st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
    st.chat_message("assistant").write(response["answer"])