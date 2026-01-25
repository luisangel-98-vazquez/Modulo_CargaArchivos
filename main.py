from processor import DocumentProcessor

def main():
    # Instanciamos el procesador
    processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)

    # --- PRUEBA 1: Archivo Markdown (Crea uno de prueba si no tienes) ---
    # Crearemos un archivo dummy para probar
    with open("prueba.md", "w", encoding="utf-8") as f:
        f.write("# Introducción a RAG\n\nRAG significa Retrieval Augmented Generation.\n\n## Ventajas\n\n1. Menor alucinación.\n2. Datos actualizados.\n\n## Desventajas\n\nRequiere infraestructura vectorial.")
    
    try:
        chunks_md = processor.process_file("prueba.md")
        print(f"\n✅ Markdown procesado. Total chunks: {len(chunks_md)}")
        for i, chunk in enumerate(chunks_md):
            print(f"\n--- Chunk {i+1} (Metadatos: {chunk.metadata}) ---")
            print(chunk.page_content)
    except Exception as e:
        print(f"Error MD: {e}")

    # --- PRUEBA 2: Archivo PDF ---
    # Asegúrate de tener un archivo 'documento.pdf' en la carpeta o cambia el nombre
    pdf_path = "tu_archivo.pdf" 
    
    # Solo intentamos si el archivo existe para no dar error en el ejemplo
    import os
    if os.path.exists(pdf_path):
        chunks_pdf = processor.process_file(pdf_path)
        print(f"\n✅ PDF procesado. Total chunks: {len(chunks_pdf)}")
        print(f"Muestra del primer chunk:\n{chunks_pdf[0].page_content[:200]}...")
    else:
        print(f"\n⚠️ No se encontró '{pdf_path}' para la prueba de PDF.")

if __name__ == "__main__":
    main()