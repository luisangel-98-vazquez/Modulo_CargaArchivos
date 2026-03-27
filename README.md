# 🤖 RAG Chatbot — Sistema de consulta de documentos PDF

Sistema de chatbot con **Retrieval-Augmented Generation (RAG)** que permite hacer preguntas en lenguaje natural sobre tus propios documentos PDF, todo corriendo **100% de forma local** en tu PC con Windows.

---

## 📐 Arquitectura del sistema

```
mis_documentos/
   └── *.pdf  →  [PyPDF Loader]  →  [Chunking]  →  [OllamaEmbeddings]
                                                          ↓
                                                    [ChromaDB]
                                                          ↓
Tu pregunta  →  [Retriever]  →  [LLM Ollama llama3]  →  Respuesta
```

### Flujo paso a paso

| Paso | Componente | Qué hace |
|------|-----------|----------|
| 1 | `PyPDFLoader` | Lee todos los PDFs de tu carpeta |
| 2 | `RecursiveCharacterTextSplitter` | Divide el texto en fragmentos de ~800 chars |
| 3 | `OllamaEmbeddings` | Convierte cada fragmento en un vector numérico |
| 4 | `ChromaDB` | Almacena los vectores en disco (persiste entre sesiones) |
| 5 | `Retriever` | Busca los fragmentos más relevantes a tu pregunta |
| 6 | `Ollama LLM` | Genera la respuesta usando el contexto recuperado |
| 7 | `Streamlit` | Muestra la interfaz de chat en el navegador |

---

## 📁 Estructura del proyecto

```
rag_chatbot/
├── app.py              ← Interfaz Streamlit (frontend del chat)
├── rag_engine.py       ← Motor RAG (toda la lógica de LangChain)
├── requirements.txt    ← Dependencias de Python
├── README.md           ← Este archivo
├── chroma_db/          ← Base de datos vectorial (se crea automáticamente)
└── mis_documentos/     ← ⚠️ TUS PDFs van aquí (o cambia la ruta en rag_engine.py)
```

---

## 🛠️ Requisitos previos

### 1. Python 3.10 o superior
Descarga desde: https://www.python.org/downloads/

### 2. Ollama (para correr el LLM localmente)

1. Descarga Ollama desde: https://ollama.com/download
2. Instálalo y ábrelo (queda corriendo en segundo plano)
3. Abre una terminal y descarga el modelo:

```bash
ollama pull llama3
```

> 💡 El modelo pesa ~4GB. También puedes usar `mistral` o `phi3` si tienes menos RAM.

---

## 🚀 Instalación

### Paso 1 — Clonar o descargar el proyecto

Coloca todos los archivos en una carpeta, por ejemplo:
```
C:\MisProyectos\rag_chatbot\
```

### Paso 2 — Crear entorno virtual (recomendado)

Abre una terminal (CMD o PowerShell) en la carpeta del proyecto:

```bash
python -m venv venv
venv\Scripts\activate
```

### Paso 3 — Instalar dependencias

```bash
pip install -r requirements.txt
```

> ⏳ Esto puede tardar unos minutos la primera vez.

### Paso 4 — Colocar tus documentos PDF

Copia tus archivos `.pdf` en la carpeta `mis_documentos/`, o actualiza la variable `DOCS_PATH` en `rag_engine.py`:

```python
DOCS_PATH = r"C:\TuRuta\mis_documentos"
```

---

## ▶️ Ejecutar el chatbot

Con el entorno virtual activado y Ollama corriendo, ejecuta:

```bash
streamlit run app.py
```

Se abrirá automáticamente en tu navegador en: **http://localhost:8501**

---

## 💬 Cómo usar la interfaz

```
┌─────────────────────┬──────────────────────────────────┐
│      SIDEBAR        │         ÁREA DE CHAT             │
│                     │                                  │
│ 📁 Ruta de PDFs     │  ← Historial de conversación     │
│ 🧠 Modelo Ollama    │                                  │
│ [📥 Cargar docs]    │                                  │
│ [🗑️ Limpiar chat]   │                                  │
│                     │                                  │
│ 📊 Estado:          │  Escribe tu pregunta aquí...  ↵  │
│   ● ACTIVO          │                                  │
│   12 páginas        │                                  │
│   38 fragmentos     │                                  │
└─────────────────────┴──────────────────────────────────┘
```

1. **Primera vez**: Haz clic en **📥 Cargar docs** — esto procesa tus PDFs y crea la base vectorial
2. **Siguientes veces**: El vectorstore se carga automáticamente desde disco (más rápido)
3. **Escribe tu pregunta** en el input inferior y presiona Enter
4. El asistente responde y muestra las **fuentes** (nombre del PDF y página)

---

## ⚙️ Configuración avanzada

Edita `rag_engine.py` para ajustar los parámetros:

```python
# Modelo de Ollama a usar
OLLAMA_MODEL = "llama3"        # Opciones: mistral, phi3, gemma2, etc.

# Tamaño de los fragmentos de texto
chunk_size=800                  # Aumenta para más contexto por chunk
chunk_overlap=100               # Overlap entre chunks adyacentes

# Número de fragmentos a recuperar por consulta
search_kwargs={"k": 4}         # Aumenta para más contexto (más lento)
```

---

## 🐛 Solución de problemas

| Problema | Solución |
|----------|----------|
| `Connection refused` al cargar docs | Verifica que Ollama esté corriendo (`ollama serve`) |
| `No PDFs found` | Revisa la ruta en `DOCS_PATH` o en el sidebar |
| Respuestas lentas | Normal la primera vez; las siguientes son más rápidas |
| `ModuleNotFoundError` | Activa el entorno virtual: `venv\Scripts\activate` |
| La interfaz no abre | Prueba manualmente: http://localhost:8501 |

---

## 📦 Dependencias principales

| Librería | Versión | Función |
|----------|---------|---------|
| `streamlit` | ≥1.35 | Interfaz web del chat |
| `langchain` | ≥0.2 | Orquestación del pipeline RAG |
| `langchain-community` | ≥0.2 | Integraciones con Ollama y ChromaDB |
| `chromadb` | ≥0.5 | Base de datos vectorial local |
| `pypdf` | ≥4.0 | Lectura de archivos PDF |
| `ollama` | ≥0.2 | Cliente para el LLM local |

---

## 🔐 Privacidad

Todo corre **completamente local** en tu PC:
- Los PDFs **nunca salen** de tu computadora
- El LLM corre offline con Ollama
- No se necesita ninguna API key ni conexión a internet (después de instalar)

---

*Proyecto desarrollado como parte del 8vo Cuatrimestre — Desarrollo Web Profesional*
