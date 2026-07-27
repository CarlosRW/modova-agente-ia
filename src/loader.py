# -*- coding: utf-8 -*-
"""
Módulo de carga y procesamiento de documentos.

Lee el PDF de documentación de Modova, lo divide en fragmentos (chunks)
y genera/guarda un índice vectorial FAISS usando embeddings de Google Gemini.
Este vectorstore es la base del sistema RAG del agente.
"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

DATA_PATH = "data/Modova_Documentacion_Interna.pdf"
VECTORSTORE_PATH = "vectorstore/faiss_index"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150


def cargar_documento(path: str = DATA_PATH):
    """Carga el PDF y lo devuelve como lista de documentos (uno por página)."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"No se encontró el documento en '{path}'. "
            "Verifica que el PDF esté en la carpeta 'data/'."
        )
    loader = PyPDFLoader(path)
    documentos = loader.load()
    print(f"✅ Documento cargado: {len(documentos)} páginas.")
    return documentos


def dividir_en_fragmentos(documentos):
    """Divide los documentos en fragmentos más pequeños (chunks) con solapamiento."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    fragmentos = splitter.split_documents(documentos)
    print(f"✅ Documento dividido en {len(fragmentos)} fragmentos.")
    return fragmentos


def crear_vectorstore(fragmentos, guardar: bool = True):
    """Genera embeddings para los fragmentos y crea el índice vectorial FAISS."""
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(fragmentos, embeddings)
    print("✅ Vectorstore FAISS creado en memoria.")

    if guardar:
        os.makedirs("vectorstore", exist_ok=True)
        vectorstore.save_local(VECTORSTORE_PATH)
        print(f"✅ Vectorstore guardado en '{VECTORSTORE_PATH}'.")

    return vectorstore


def cargar_vectorstore_existente():
    """Carga un vectorstore FAISS previamente guardado en disco."""
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def obtener_vectorstore():
    """
    Punto de entrada principal: si ya existe un vectorstore guardado, lo carga;
    si no, procesa el documento desde cero y lo crea.
    """
    if os.path.exists(VECTORSTORE_PATH):
        print("📂 Vectorstore existente encontrado. Cargando desde disco...")
        return cargar_vectorstore_existente()

    print("⚙️  No hay vectorstore previo. Procesando documento desde cero...")
    documentos = cargar_documento()
    fragmentos = dividir_en_fragmentos(documentos)
    return crear_vectorstore(fragmentos)


if __name__ == "__main__":
    # Permite ejecutar este archivo directamente para (re)generar el índice:
    # python src/loader.py
    documentos = cargar_documento()
    fragmentos = dividir_en_fragmentos(documentos)
    crear_vectorstore(fragmentos)