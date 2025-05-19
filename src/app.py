import streamlit as st
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
import os
import langchain
from rag import RAG_tool

# --- Habilitar Langsmith ---
langchain.debug = True
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "Chatbot-RAG"

# --- Inicialización ---
if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# --- Streamlit app ---
st.set_page_config(page_title="Chatbot", page_icon=":robot_face:")

# --- Barra lateral para carga de PDF y configuración ---
st.sidebar.header("Carga de PDF y Configuración")
uploaded_file = st.sidebar.file_uploader("Sube un archivo PDF", type=["pdf"], key="file_uploader")

default_model = RAG_tool.DEFAULT_MODEL
default_temp = 0.7
default_top_p = 0.9
default_top_k = 50

model_name = st.sidebar.text_input("Modelo Ollama", value=default_model, disabled=True)
temperature = st.sidebar.slider("Temperatura", 0.0, 1.0, default_temp, 0.01)
top_p = st.sidebar.slider("Top P", 0.0, 1.0, default_top_p, 0.01)
top_k = st.sidebar.slider("Top K", 1, 100, default_top_k, 1)

if "rag_tool" not in st.session_state:
    st.session_state["rag_tool"] = RAG_tool()  # Inicializar RAG_tool

if "pdf_processed" not in st.session_state:
    st.session_state["pdf_processed"] = False
if "uploaded_file_name" not in st.session_state:
    st.session_state["uploaded_file_name"] = None

def process_pdf_and_config():
    """
    Función para procesar el PDF y aplicar la configuración.
    Se llama al hacer clic en el botón "Aplicar Configuración".
    """
    if uploaded_file is not None:
        # Solo procesar si es un nuevo archivo o no se ha procesado antes
        if not st.session_state["pdf_processed"] or uploaded_file.name != st.session_state["uploaded_file_name"]:
            with st.spinner("Procesando el PDF..."):
                # Inicializar el LLM con los parámetros seleccionados
                st.session_state["rag_tool"].initialize_llm_with_params(model_name, temperature, top_p, top_k)
                vectordb = st.session_state["rag_tool"].process_pdf_and_create_vector_store(uploaded_file)
                if vectordb:
                    st.session_state["vectordb"] = vectordb
                    st.session_state["rag_chain"] = st.session_state["rag_tool"].setup_rag_chain(
                        st.session_state["vectordb"]
                    )
                    st.session_state["knowledge_base_loaded"] = True
                    st.session_state["pdf_processed"] = True
                    st.session_state["uploaded_file_name"] = uploaded_file.name  # Guardar el nombre del archivo
                else:
                    st.error("No se pudo crear la base de datos vectorial.")
        else:
            # Si el PDF no ha cambiado, solo actualizar la cadena RAG con la nueva configuración.
            st.session_state["rag_tool"].initialize_llm_with_params(model_name, temperature, top_p, top_k)
            st.session_state["rag_chain"] = st.session_state["rag_tool"].setup_rag_chain(
                st.session_state.get("vectordb")
            )
            st.info("Solo se aplicó la configuración del modelo.")

    elif not st.session_state["knowledge_base_loaded"]:
        st.info("Cargue un archivo PDF y haga clic en 'Aplicar Configuración'.")
    else:
        st.session_state["rag_tool"].initialize_llm_with_params(model_name, temperature, top_p, top_k)
        st.session_state["rag_chain"] = st.session_state["rag_tool"].setup_rag_chain(
                st.session_state.get("vectordb")
            )
        st.info("Se aplicó la configuración del modelo.")

st.sidebar.button("Aplicar Configuración", on_click=process_pdf_and_config)


# --- Chat Interface ---
st.title("Chatbot con RAG")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Say something"):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        if st.session_state.get("knowledge_base_loaded") and st.session_state.get("rag_chain"):
            response = st.session_state["rag_tool"].get_rag_response(
                st.session_state["rag_chain"], prompt
            )
        else:
            response = st.session_state["agent"].run(input=prompt)

    st.session_state["messages"].append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
