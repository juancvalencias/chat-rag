import streamlit as st
from rag import RAG_tool

st.title("Prueba de Carga de PDF")

pdf_loader = RAG_tool()  
uploaded_file = st.file_uploader("Sube un archivo PDF para probar la carga", type=["pdf"])

if uploaded_file is not None:
    st.subheader("Información del Archivo Cargado:")
    st.write(f"Nombre del archivo: {uploaded_file.name}")
    st.write(f"Tipo de archivo: {uploaded_file.type}")
    st.write(f"Tamaño del archivo: {uploaded_file.size} bytes")

    if st.button("Procesar PDF"):
        with st.spinner("Procesando..."):
            temp_file_path = f"./temp_test_{uploaded_file.name}"
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.read())
            try:
                documents = pdf_loader.load_and_process_pdf(temp_file_path)  
                st.success(f"PDF procesado. Se encontraron {len(documents)} documentos/fragmentos.")
                if documents:
                    st.subheader("Primeros Fragmentos:")
                    for i, doc in enumerate(documents[:10]):
                        st.write(f"Fragmento {i+1}:")
                        st.info(doc.page_content[:200] + "...")
            except Exception as e:
                st.error(f"Error al procesar el PDF: {e}")
            finally:
                import os
                os.remove(temp_file_path)