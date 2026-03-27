import streamlit as st
import os
import sys

st.set_page_config(
    page_title="FitCoach AI",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
)

sys.path.append(os.path.dirname(__file__))
from RAGEngine import RAGEngine, DOCS_PATH, OLLAMA_MODEL

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] { font-family: 'Barlow', sans-serif; }
    .stApp { background: #0b0f1a; color: #dce3ef; }

    section[data-testid="stSidebar"] {
        background: #0e1420 !important;
        border-right: 2px solid #1a2744;
    }

    .fitcoach-header {
        display: flex; align-items: center; gap: 14px;
        padding: 18px 0 14px 0;
        border-bottom: 2px solid #1e3a6e;
        margin-bottom: 24px;
    }
    .fitcoach-logo {
        width: 52px; height: 52px;
        background: linear-gradient(135deg, #1a56db, #0ea5e9);
        border-radius: 14px; display: flex; align-items: center;
        justify-content: center; font-size: 1.7rem; flex-shrink: 0;
        box-shadow: 0 4px 18px rgba(26,86,219,0.45);
    }
    .fitcoach-name {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.9rem; font-weight: 800; color: #fff;
        letter-spacing: 1.5px; line-height: 1; text-transform: uppercase;
    }
    .fitcoach-name span { color: #38bdf8; }
    .fitcoach-tagline {
        font-size: 0.73rem; color: #3a5070;
        letter-spacing: 2px; text-transform: uppercase;
        font-weight: 600; margin-top: 4px;
    }

    .sidebar-logo {
        display: flex; align-items: center; gap: 10px;
        padding: 14px 0; border-bottom: 1px solid #1a2744; margin-bottom: 14px;
    }
    .sidebar-logo-icon {
        width: 36px; height: 36px;
        background: linear-gradient(135deg, #1a56db, #0ea5e9);
        border-radius: 9px; display: flex; align-items: center;
        justify-content: center; font-size: 1.1rem;
        box-shadow: 0 2px 10px rgba(26,86,219,0.35);
    }
    .sidebar-brand-name {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.3rem; font-weight: 800; color: #fff;
        text-transform: uppercase; letter-spacing: 1px;
    }
    .sidebar-brand-name span { color: #38bdf8; }

    .section-label {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.68rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: 2.5px; color: #1a56db;
        margin: 16px 0 8px 0;
        display: flex; align-items: center; gap: 7px;
    }
    .section-label::after {
        content: ''; flex: 1; height: 1px; background: #1a2744;
    }

    .chat-row-user {
        display: flex; justify-content: flex-end;
        margin: 10px 0 4px 0;
        animation: slideInRight 0.18s ease;
    }
    .chat-row-assistant {
        display: flex; justify-content: flex-start;
        margin: 10px 0 4px 0; gap: 10px; align-items: flex-start;
        animation: slideInLeft 0.18s ease;
    }
    @keyframes slideInRight {
        from { opacity:0; transform: translateX(10px); }
        to   { opacity:1; transform: translateX(0); }
    }
    @keyframes slideInLeft {
        from { opacity:0; transform: translateX(-10px); }
        to   { opacity:1; transform: translateX(0); }
    }

    .msg-user {
        background: linear-gradient(135deg, #1a56db, #1e40af);
        border-radius: 18px 18px 4px 18px;
        padding: 12px 18px; max-width: 70%;
        color: #e8f0fe; font-size: 0.95rem; line-height: 1.65;
        box-shadow: 0 3px 14px rgba(26,86,219,0.3);
    }
    .bot-avatar {
        width: 34px; height: 34px;
        background: linear-gradient(135deg, #0f172a, #1e3a5f);
        border: 2px solid #1a56db; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 1rem; flex-shrink: 0; margin-top: 2px;
    }
    .msg-assistant {
        background: #111827; border: 1px solid #1e3a5f;
        border-radius: 4px 18px 18px 18px;
        padding: 13px 18px; max-width: 76%;
        color: #dce3ef; font-size: 0.95rem; line-height: 1.7;
        box-shadow: 0 3px 12px rgba(0,0,0,0.25);
    }

    .sources-badge {
        background: #080e1a; border: 1px solid #1a3a5c;
        border-left: 3px solid #0ea5e9;
        border-radius: 0 6px 6px 0;
        padding: 5px 12px; margin-top: 4px; margin-left: 44px;
        font-size: 0.74rem; color: #38bdf8; max-width: 76%;
    }

    .status-pill {
        display: inline-flex; align-items: center; gap: 6px;
        border-radius: 999px; padding: 4px 12px;
        font-size: 0.7rem; font-family: 'Barlow Condensed', sans-serif;
        font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
    }
    .status-active  { background: #052e16; color: #4ade80; border: 1px solid #166534; }
    .status-inactive{ background: #1c0a0a; color: #f87171; border: 1px solid #7f1d1d; }
    .status-dot {
        width: 7px; height: 7px; border-radius: 50%;
        background: currentColor; animation: blink 2s infinite;
    }
    @keyframes blink {
        0%,100%{opacity:1;} 50%{opacity:0.3;}
    }

    .stat-card {
        background: #0b0f1a; border: 1px solid #1a2744;
        border-top: 2px solid #1a56db; border-radius: 8px;
        padding: 10px 14px; margin: 5px 0;
    }
    .stat-value {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.9rem; font-weight: 800; color: #38bdf8; line-height: 1;
    }
    .stat-label {
        font-size: 0.67rem; color: #3a5070; text-transform: uppercase;
        letter-spacing: 1.5px; font-weight: 600; margin-top: 2px;
    }

    .welcome-card {
        background: linear-gradient(135deg, #0d1525 0%, #0f1e38 100%);
        border: 1px solid #1e3a6e; border-radius: 16px;
        padding: 36px 28px; text-align: center;
        margin: 30px auto; max-width: 520px;
    }
    .welcome-icon { font-size: 3rem; margin-bottom: 14px; }
    .welcome-title {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.5rem; font-weight: 800; color: #fff;
        text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px;
    }
    .welcome-text { font-size: 0.9rem; color: #3a5070; line-height: 1.7; }
    .welcome-hint {
        display: inline-block; background: #0c1628;
        border: 1px solid #1a56db; color: #38bdf8;
        border-radius: 6px; padding: 5px 14px;
        font-size: 0.78rem; font-weight: 600; margin-top: 16px; letter-spacing: 0.5px;
    }

    .stButton > button {
        background: linear-gradient(135deg, #1a56db, #1d4ed8) !important;
        color: white !important; border: none !important;
        border-radius: 8px !important;
        font-family: 'Barlow Condensed', sans-serif !important;
        font-size: 0.82rem !important; font-weight: 700 !important;
        letter-spacing: 1px !important; text-transform: uppercase !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1e40af, #1a56db) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 14px rgba(26,86,219,0.4) !important;
    }

    .stChatInput > div {
        background: #111827 !important;
        border: 1.5px solid #1a2f56 !important;
        border-radius: 12px !important;
    }
    .stChatInput textarea {
        color: #dce3ef !important;
        font-family: 'Barlow', sans-serif !important;
        font-size: 0.95rem !important;
    }
    .stTextInput > div > div > input {
        background: #080e1a !important; color: #dce3ef !important;
        border: 1px solid #1a2744 !important; border-radius: 8px !important;
        font-family: 'Barlow', sans-serif !important; font-size: 0.85rem !important;
    }

    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    hr { border-color: #1a2744 !important; }
    .stSpinner > div { border-top-color: #1a56db !important; }
</style>
""", unsafe_allow_html=True)

# ── Estado de sesión ──
if "engine"      not in st.session_state: st.session_state.engine      = RAGEngine()
if "messages"    not in st.session_state: st.session_state.messages    = []
if "initialized" not in st.session_state: st.session_state.initialized = False
if "stats"       not in st.session_state: st.session_state.stats       = {}

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">💪</div>
        <div class="sidebar-brand-name">Fit<span>Coach</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">⚙ Configuración</div>', unsafe_allow_html=True)
    docs_path  = st.text_input("Carpeta de documentos", value=DOCS_PATH,    help="Ruta con tus PDFs")
    model_name = st.text_input("Modelo Ollama",          value=OLLAMA_MODEL, help="ej: llama3.2, mistral")

    st.markdown('<div class="section-label">⚡ Acciones</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: load_btn  = st.button("📥 Cargar",  use_container_width=True)
    with col2: clear_btn = st.button("🗑 Limpiar", use_container_width=True)

    if load_btn:
        with st.spinner("Procesando documentos..."):
            try:
                engine = RAGEngine()
                stats  = engine.initialize(docs_path)
                st.session_state.engine      = engine
                st.session_state.initialized = True
                st.session_state.stats       = stats
                st.session_state.messages    = []
                st.success("✅ Documentos cargados")
            except Exception as e:
                st.error(f"❌ {e}")
                st.session_state.initialized = False

    if clear_btn:
        st.session_state.messages = []
        st.rerun()

    if not st.session_state.initialized:
        if st.session_state.engine.load_existing_vectorstore():
            st.session_state.initialized = True

    st.markdown('<div class="section-label">📊 Sistema</div>', unsafe_allow_html=True)

    if st.session_state.initialized:
        st.markdown('<div class="status-pill status-active"><span class="status-dot"></span> Sistema activo</div>', unsafe_allow_html=True)
        stats = st.session_state.stats
        if stats:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{stats.get("paginas_cargadas","—")}</div>
                <div class="stat-label">Páginas cargadas</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats.get("fragmentos_creados","—")}</div>
                <div class="stat-label">Fragmentos indexados</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="stat-card"><div class="stat-value">✓</div><div class="stat-label">Vectorstore listo</div></div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{len(st.session_state.messages)//2}</div>
            <div class="stat-label">Consultas en sesión</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-pill status-inactive"><span class="status-dot"></span> Sin documentos</div>', unsafe_allow_html=True)
        st.caption("Carga tus PDFs para comenzar.")

    st.markdown("---")
    st.markdown('<div style="font-size:0.67rem;color:#1e3050;line-height:2.2;letter-spacing:0.5px;">MOTOR · Ollama (local)<br>VECTOR DB · ChromaDB<br>FRAMEWORK · LangChain</div>', unsafe_allow_html=True)

# ── ÁREA PRINCIPAL ──
st.markdown("""
<div class="fitcoach-header">
    <div class="fitcoach-logo">💪</div>
    <div>
        <div class="fitcoach-name">Fit<span>Coach</span> AI</div>
        <div class="fitcoach-tagline">Tu asistente de entrenamiento inteligente</div>
    </div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.messages:
    if st.session_state.initialized:
        st.markdown("""
        <div class="welcome-card">
            <div class="welcome-icon">🏋️</div>
            <div class="welcome-title">Sistema listo</div>
            <div class="welcome-text">Puedes preguntarme sobre rutinas de entrenamiento,<br>nutrición deportiva, técnicas y más.</div>
            <span class="welcome-hint">✦ Escribe tu consulta abajo</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="welcome-card">
            <div class="welcome-icon">📂</div>
            <div class="welcome-title">Carga tus documentos</div>
            <div class="welcome-text">Agrega tus PDFs de fitness en la carpeta configurada<br>y presiona <strong style="color:#38bdf8">Cargar</strong> en el panel izquierdo.</div>
            <span class="welcome-hint">← Panel de configuración</span>
        </div>
        """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-row-user"><div class="msg-user">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-row-assistant"><div class="bot-avatar">🤖</div><div class="msg-assistant">{msg["content"]}</div></div>', unsafe_allow_html=True)
        if msg.get("sources"):
            st.markdown(f'<div class="sources-badge">📄 {" · ".join(msg["sources"])}</div>', unsafe_allow_html=True)

# ── INPUT ──
if prompt := st.chat_input("Pregunta sobre entrenamiento, nutrición, rutinas...", disabled=not st.session_state.initialized):
    st.markdown(f'<div class="chat-row-user"><div class="msg-user">{prompt}</div></div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Analizando documentos..."):
        try:
            result = st.session_state.engine.query(prompt)
            answer, sources = result["answer"], result["sources"]
        except Exception as e:
            answer, sources = f"Error al consultar: {e}", []

    st.markdown(f'<div class="chat-row-assistant"><div class="bot-avatar">🤖</div><div class="msg-assistant">{answer}</div></div>', unsafe_allow_html=True)
    if sources:
        st.markdown(f'<div class="sources-badge">📄 {" · ".join(sources)}</div>', unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})