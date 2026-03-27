import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# ==========================================
# CONFIGURACIÓN GLOBAL
# ==========================================
DOCS_PATH = r"C:\Users\luisa\Music\Cuatrimestre_8\project_RAG\rag_venv\documentos"
CHROMA_DB_PATH = "./chroma_db"
OLLAMA_MODEL = "llama3"

# ==========================================
# CLASE PRINCIPAL DEL MOTOR RAG
# ==========================================
class RAGEngine:
    def __init__(self):
        self.rag_chain = None
        self.vectorstore = None
        self.docs_loaded = 0
        self.chunks_created = 0

    def initialize(self, docs_path: str = DOCS_PATH) -> dict:
        """
        Inicializa el motor RAG completo:
        carga PDFs → chunking → embeddings → vectorstore → chain
        Retorna un dict con estadísticas del proceso.
        """
        status = {}

        # PASO 1: Cargar documentos PDF
        loader = DirectoryLoader(
            docs_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        docs = loader.load()
        self.docs_loaded = len(docs)
        status["paginas_cargadas"] = self.docs_loaded

        if self.docs_loaded == 0:
            raise ValueError(f"No se encontraron PDFs en: {docs_path}")

        # PASO 2: Chunking
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )
        splits = splitter.split_documents(docs)
        self.chunks_created = len(splits)
        status["fragmentos_creados"] = self.chunks_created

        # PASO 3: Embeddings + Vectorstore (persiste en disco)
        embeddings = OllamaEmbeddings(model=OLLAMA_MODEL)
        self.vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=CHROMA_DB_PATH
        )
        status["vectorstore"] = "listo"

        # PASO 4: Prompt
        system_prompt = (
            "Eres un asistente experto y amigable. Responde SIEMPRE en español. "
            "Usa únicamente el siguiente contexto para responder:\n\n{context}\n\n"
            "Si la información no está en el contexto, responde exactamente: "
            "'Lo siento, esa información no está disponible en los documentos cargados.'"
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

        # PASO 5: LLM + Chain (LCEL — sin langchain.chains)
        llm = OllamaLLM(model=OLLAMA_MODEL)
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})

        def format_docs(docs):
            self._last_docs = docs  # guardar para extraer fuentes después
            return "\n\n".join(doc.page_content for doc in docs)

        self.rag_chain = (
            {
                "context": retriever | format_docs,
                "input": RunnablePassthrough()
            }
            | prompt
            | llm
            | StrOutputParser()
        )
        self._retriever = retriever
        self._last_docs = []
        status["chain"] = "configurada"

        return status

    def load_existing_vectorstore(self) -> bool:
        """
        Intenta cargar un vectorstore ya existente en disco.
        Retorna True si lo encuentra, False si no.
        """
        if not os.path.exists(CHROMA_DB_PATH):
            return False

        embeddings = OllamaEmbeddings(model=OLLAMA_MODEL)
        self.vectorstore = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embeddings
        )

        system_prompt = (
            "Eres un asistente experto y amigable. Responde SIEMPRE en español. "
            "Usa únicamente el siguiente contexto para responder:\n\n{context}\n\n"
            "Si la información no está en el contexto, responde exactamente: "
            "'Lo siento, esa información no está disponible en los documentos cargados.'"
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

        llm = OllamaLLM(model=OLLAMA_MODEL)
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})

        def format_docs(docs):
            self._last_docs = docs
            return "\n\n".join(doc.page_content for doc in docs)

        self.rag_chain = (
            {
                "context": retriever | format_docs,
                "input": RunnablePassthrough()
            }
            | prompt
            | llm
            | StrOutputParser()
        )
        self._retriever = retriever
        self._last_docs = []
        return True

    def query(self, user_input: str) -> dict:
        """
        Realiza una consulta al sistema RAG.
        Retorna la respuesta y los documentos fuente usados.
        """
        if self.rag_chain is None:
            raise RuntimeError("El motor RAG no está inicializado. Carga los documentos primero.")

        # Primero recuperar los docs para las fuentes
        docs = self._retriever.invoke(user_input)

        # Luego obtener la respuesta
        answer = self.rag_chain.invoke(user_input)

        # Extraer fuentes únicas
        sources = []
        for doc in docs:
            src = doc.metadata.get("source", "Desconocido")
            page = doc.metadata.get("page", "?")
            entry = f"{os.path.basename(src)} (pág. {page + 1})"
            if entry not in sources:
                sources.append(entry)

        return {
            "answer": answer,
            "sources": sources
        }