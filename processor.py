import os
from langchain_community.document_loaders import PyPDFLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        """
        Configuración inicial para el chunking.
        chunk_size: Tamaño objetivo de cada fragmento.
        chunk_overlap: Solapamiento para no perder contexto entre cortes.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def process_file(self, file_path):
        """
        Identifica la extensión y delega la tarea.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo {file_path} no existe.")

        extension = os.path.splitext(file_path)[1].lower()

        if extension == '.md':
            return self._process_markdown(file_path)
        elif extension == '.pdf':
            return self._process_pdf(file_path)
        else:
            raise ValueError(f"Formato {extension} no soportado. Use .pdf o .md")

    def _process_markdown(self, file_path):
        """
        Estrategia Lógica: Divide basándose en la jerarquía de encabezados (#, ##, ###).
        Esto garantiza que una sección completa se mantenga junta.
        """
        print(f"--- Procesando Markdown: {file_path} ---")
        
        # 1. Leer el archivo como texto plano primero
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_text = f.read()

        # 2. Definir los separadores lógicos
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]

        # 3. Dividir por estructura
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        md_header_splits = markdown_splitter.split_text(markdown_text)

        # 4. (Opcional) Si una sección es GIGANTE, aplicamos un corte recursivo adicional
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        final_chunks = text_splitter.split_documents(md_header_splits)
        
        return final_chunks

    def _process_pdf(self, file_path):
        """
        Estrategia Recursiva: Intenta cortar primero por parrafos dobles, luego simples,
        luego espacios, manteniendo la semántica lo mejor posible.
        """
        print(f"--- Procesando PDF: {file_path} ---")
        
        # 1. Cargar el PDF
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        # 2. Configurar el splitter recursivo
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""] # Prioridad de corte
        )

        # 3. Dividir
        final_chunks = text_splitter.split_documents(documents)
        
        return final_chunks