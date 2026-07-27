# -*- coding: utf-8 -*-
"""
Agente de IA con arquitectura RAG (Retrieval-Augmented Generation).

Recibe una pregunta en lenguaje natural, recupera los fragmentos más
relevantes del vectorstore de Modova y genera una respuesta usando
Google Gemini, basada exclusivamente en el contenido de los documentos.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.loader import obtener_vectorstore

load_dotenv()

# Cantidad de fragmentos relevantes a recuperar por pregunta
TOP_K = 4

PROMPT_TEMPLATE = """Eres el asistente virtual oficial de Modova, una tienda
online de ropa. Tu trabajo es responder preguntas de clientes basándote
ÚNICAMENTE en el siguiente contexto extraído de la documentación oficial
de la empresa.

Reglas:
- Responde de forma clara, breve y amable, como lo haría un agente de
  atención al cliente.
- Si la información no está en el contexto, responde exactamente:
  "No tengo esa información en la documentación disponible. Te recomiendo
  contactar directamente a soporte@modova.com."
- No inventes políticas, plazos, precios ni datos que no aparezcan en el contexto.
- Si es pertinente, menciona plazos o porcentajes exactos tal como aparecen
  en el contexto.

Contexto:
{context}

Pregunta del cliente:
{pregunta}

Respuesta:"""


def formatear_contexto(documentos):
    """Concatena el contenido de los fragmentos recuperados en un solo texto."""
    return "\n\n---\n\n".join(doc.page_content for doc in documentos)


def crear_cadena_rag():
    """Construye la cadena (chain) completa de RAG usando LangChain Expression Language."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "No se encontró GROQ_API_KEY. Define tu clave en el archivo .env"
        )

    vectorstore = obtener_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        api_key=api_key,
        temperature=0.2,
    )

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    cadena = (
        {
            "context": retriever | formatear_contexto,
            "pregunta": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return cadena


class AgenteModova:
    """
    Envoltorio simple sobre la cadena RAG para mantener el estado
    (evita reconstruir el vectorstore y el LLM en cada pregunta).
    """

    def __init__(self):
        print("🔧 Inicializando agente de Modova...")
        self.cadena = crear_cadena_rag()
        print("✅ Agente listo para responder preguntas.")

    def preguntar(self, pregunta: str) -> str:
        if not pregunta or not pregunta.strip():
            return "Por favor, escribe una pregunta válida."
        return self.cadena.invoke(pregunta)


if __name__ == "__main__":
    # Modo de prueba por consola: python src/agent.py
    agente = AgenteModova()
    print("\n💬 Agente de Modova listo. Escribe 'salir' para terminar.\n")

    while True:
        pregunta = input("Tú: ")
        if pregunta.strip().lower() in ("salir", "exit", "quit"):
            print("👋 ¡Hasta luego!")
            break
        respuesta = agente.preguntar(pregunta)
        print(f"\nAgente Modova: {respuesta}\n")