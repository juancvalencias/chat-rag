import streamlit as st
from langchain_community.vectorstores import Chroma
from rag import RAG_tool

st.title("Prueba de Generación de Embeddings")


rag_tool = RAG_tool()

# Verificar si los embeddings se inicializaron correctamente
if rag_tool.embeddings is None:
    st.error("Error al inicializar los embeddings en la clase RAG_tool.")
    st.stop()
else:
    st.success("Embeddings inicializados correctamente a través de la clase RAG_tool.")

st.subheader("Generar Embeddings para un Texto de Prueba")
test_text = st.text_area("Introduce un texto para generar embeddings:", "Este es un texto de prueba para generar embeddings.")

if st.button("Generar Embedding"):
    if test_text:
        with st.spinner("Generando embedding..."):
            try:
                vector = rag_tool.embeddings.embed_query(test_text)
                st.success("Embedding generado.")
                st.write("Dimensión del embedding:", len(vector))
                st.write("Primeros 10 valores del embedding:", vector[:10])
            except Exception as e:
                st.error(f"Error al generar embedding: {e}")

st.subheader("Generar Embeddings para Múltiples Textos")
multiple_texts = st.text_area("Introduce múltiples textos (uno por línea):", "Texto uno\nTexto dos\nOtro texto")
list_of_texts = [line.strip() for line in multiple_texts.splitlines() if line.strip()]

if st.button("Generar Embeddings Múltiples"):
    if list_of_texts:
        with st.spinner("Generando embeddings múltiples..."):
            try:
                vectors = rag_tool.embeddings.embed_documents(list_of_texts)
                st.success(f"Se generaron {len(vectors)} embeddings.")
                for i, vector in enumerate(vectors):
                    st.write(f"Embedding para '{list_of_texts[i][:20]}...':")
                    st.write("Dimensión:", len(vector))
                    st.write("Primeros 5 valores:", vector[:5])
            except Exception as e:
                st.error(f"Error al generar embeddings múltiples: {e}")

st.subheader("Crear y Consultar una Base de Datos Vectorial de Prueba (Temporal)")
test_data = [
    "El perro ladra al cuando pasa alguien.",
    "El gato duerme en la cama de mi abuela.",
    "Los pájaros cantan por la mañana."
]

if st.button("Crear Base de Datos Vectorial de Prueba"):
    with st.spinner("Creando base de datos vectorial temporal..."):
        try:
            st.session_state["vectordb_test"] = Chroma.from_texts(texts=test_data, embedding=rag_tool.embeddings)
            st.session_state["test_vectordb_created"] = True
            st.success("Base de datos vectorial temporal de prueba creada.")
        except Exception as e:
            st.error(f"Error al crear la base de datos vectorial temporal: {e}")

query_text = st.text_input("Introduce una consulta para buscar en la base de datos temporal:", "animales")

if st.button("Buscar en la Base de Datos Temporal"):
    if "vectordb_test" in st.session_state and st.session_state.get("test_vectordb_created"):
        with st.spinner("Buscando..."):
            try:
                results = st.session_state["vectordb_test"].similarity_search(query_text, k=2)
                st.subheader("Resultados de la Búsqueda Temporal:")
                for doc in results:
                    st.info(doc.page_content)
            except Exception as e:
                st.error(f"Error al buscar en la base de datos temporal: {e}")
    else:
        st.warning("Crea primero la base de datos vectorial temporal de prueba.")

st.info("Esta prueba no persiste la base de datos vectorial en disco.")