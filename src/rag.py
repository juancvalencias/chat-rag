from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import streamlit as st

class RAG_tool:
    OLLAMA_BASE_URL = "http://localhost:11434"
    EMBEDDING_MODEL = "nomic-embed-text:latest"
    PERSIST_DIRECTORY = "chroma_db"
    DEFAULT_MODEL = "llama2:7b"

    def __init__(self):
        self.llm = self._initialize_llm()
        self.embeddings = self._initialize_embeddings()

    def _initialize_llm(self, model_name=DEFAULT_MODEL, temperature=0.7, top_p=0.9, top_k=50):
        try:
            llm = Ollama(model=model_name,
                         base_url=self.OLLAMA_BASE_URL,
                         temperature=temperature,
                         top_p=top_p,
                         top_k=top_k)
            return llm
        except Exception as e:
            st.error(f"Error loading Ollama model: {e}")
            return None

    def _initialize_embeddings(self):
        try:
            embeddings = OllamaEmbeddings(base_url=self.OLLAMA_BASE_URL, model=self.EMBEDDING_MODEL)
            return embeddings
        except Exception as e:
            st.error(f"Error loading Ollama embeddings: {e}")
            return None

    def load_and_process_pdf(self, file_path):
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(documents)
        return chunks

    def create_vector_store(self, chunks, persist_directory=PERSIST_DIRECTORY):
        vectordb = Chroma.from_documents(
            documents=chunks, embedding=self.embeddings, persist_directory=persist_directory
        )
        vectordb.persist()
        return vectordb

    def load_vector_store(self, persist_directory=PERSIST_DIRECTORY):
        if self.embeddings is None:
            self.embeddings = self._initialize_embeddings()
            if self.embeddings is None:
                return None
        try:
            vectordb = Chroma(persist_directory=persist_directory, embedding_function=self.embeddings)
            return vectordb
        except Exception as e:
            st.warning(f"No se encontró una base de conocimientos existente o hubo un error al cargarla: {e}")
            return None

    def setup_rag_chain(self, vectordb):
        if self.llm is None or vectordb is None:
            return None
        prompt_template = """Utiliza la siguiente información contextual para responder la pregunta del usuario.
        Si no sabes la respuesta, simplemente di que no lo sabes, no intentes inventar una respuesta, procura usar como idioma el español.

        Contexto: {context}
        Pregunta: {question}
        Respuesta útil:"""
        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        rag_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vectordb.as_retriever(),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=False
        )
        return rag_chain

    def process_pdf_and_create_vector_store(self, uploaded_file):
        if uploaded_file is not None and self.embeddings:
            with st.spinner("Procesando el PDF..."):
                temp_file_path = f"./temp_{uploaded_file.name}"
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.read())

                chunks = self.load_and_process_pdf(temp_file_path)
                os.remove(temp_file_path)  # Limpiar el archivo temporal

                vectordb = self.create_vector_store(chunks)
                st.success("PDF procesado y base de conocimientos creada.")
                return vectordb
        return None

    def get_rag_response(self, rag_chain, query):
        if rag_chain:
            return rag_chain.run({"query": query})
        return "La base de conocimientos no está cargada o no se pudo inicializar."

    def initialize_llm_with_params(self, model_name, temperature, top_p, top_k):
        self.llm = self._initialize_llm(model_name, temperature, top_p, top_k)
        return self.llm

    @property
    def persist_directory(self):
        return self.PERSIST_DIRECTORY