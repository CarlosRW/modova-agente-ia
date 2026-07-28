# 🛍️ Agente Modova

Agente de inteligencia artificial que responde preguntas en lenguaje natural sobre las políticas de **Modova**, una tienda online de ropa, sin necesidad de abrir ni leer manualmente los documentos. Construido con arquitectura **RAG (Retrieval-Augmented Generation)** usando LangChain.

> Proyecto desarrollado para el **Challenge Alura Agente**.

🔗 **Demo en vivo:** [https://modova-agente-ia.streamlit.app/](https://modova-agente-ia.streamlit.app/)
*(reemplaza este link por tu URL real de Streamlit Cloud si es diferente)*

---

## 📌 Descripción general

**Modova** es una tienda online de ropa (ficticia) que, como cualquier e-commerce, cuenta con documentación interna extensa: política de privacidad, política de reembolsos y devoluciones, preguntas frecuentes, guía de envíos y términos y condiciones.

En vez de obligar al cliente a leer PDFs largos, este proyecto implementa un **agente conversacional** capaz de responder preguntas puntuales ("¿cuántos días tengo para devolver un producto?", "¿hacen envíos gratis?") consultando directamente el contenido oficial de la empresa, con respuestas breves, claras y fundamentadas **únicamente** en la documentación real (evitando alucinaciones).

## 🏗️ Arquitectura de la solución

El sistema sigue un patrón **RAG (Retrieval-Augmented Generation)**:

```
┌───────────────────────┐
│  PDF documentación     │
│  interna de Modova     │
└──────────┬────────────┘
           │ 1. Carga (PyPDFLoader)
           ▼
┌───────────────────────┐
│  Fragmentación          │
│  (RecursiveCharacter    │
│   TextSplitter)         │
└──────────┬────────────┘
           │ 2. Chunks de texto
           ▼
┌───────────────────────┐
│  Embeddings locales      │
│  (sentence-transformers  │
│   all-MiniLM-L6-v2)      │
└──────────┬────────────┘
           │ 3. Vectores
           ▼
┌───────────────────────┐
│  Vectorstore FAISS        │◄── se guarda en disco tras la 1ª ejecución
└──────────┬────────────┘
           │ 4. Búsqueda semántica (top-k)
           ▼
┌───────────────────────┐        ┌─────────────────────┐
│  Pregunta del usuario    │──────▶│  Retriever (FAISS)    │
└───────────────────────┘        └──────────┬──────────┘
                                              │ contexto relevante
                                              ▼
                                   ┌─────────────────────┐
                                   │  LLM (Groq / Llama     │
                                   │  vía openai/gpt-oss)   │
                                   └──────────┬──────────┘
                                              │ respuesta
                                              ▼
                                   ┌─────────────────────┐
                                   │  Interfaz Streamlit     │
                                   └─────────────────────┘
```

**Flujo resumido:**
1. El PDF de Modova se carga y se divide en fragmentos de ~800 caracteres con solapamiento.
2. Cada fragmento se convierte en un vector numérico (embedding) usando un modelo local de `sentence-transformers` — sin depender de APIs externas de pago para esta parte.
3. Los vectores se indexan en **FAISS**, una base de datos vectorial que permite búsqueda semántica ultrarrápida.
4. Cuando el usuario hace una pregunta, el sistema busca los 4 fragmentos más relevantes del documento.
5. Esos fragmentos se envían como contexto a un modelo de lenguaje (**Llama vía Groq**), que genera la respuesta final basada solo en esa información.
6. Todo se expone a través de una interfaz de chat construida con **Streamlit**.

## 🛠️ Tecnologías y herramientas utilizadas

| Categoría | Tecnología |
|---|---|
| Lenguaje | Python 3.13+ |
| Orquestación RAG | LangChain (`langchain`, `langchain-community`) |
| Carga de PDF | PyPDFLoader (`pypdf`) |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`, local, gratuito) |
| Vectorstore | FAISS (Facebook AI Similarity Search) |
| Modelo de lenguaje (LLM) | Llama vía **Groq API** (`openai/gpt-oss-120b`) |
| Interfaz | Streamlit |
| Gestión de variables sensibles | python-dotenv |
| Deploy | Streamlit Community Cloud |

## 📂 Estructura del repositorio

```
modova-agente-ia/
├── data/
│   └── Modova_Documentacion_Interna.pdf   # Documento fuente
├── scripts/
│   └── generate_docs.py                   # Script que generó el PDF fuente
├── docs/
│   └── screenshot-deploy.png              # Evidencia del deploy
├── src/
│   ├── __init__.py
│   ├── loader.py                          # Carga, fragmentación y vectorstore
│   ├── agent.py                           # Lógica del agente RAG
│   └── app.py                             # Interfaz Streamlit
├── vectorstore/                           # Índice FAISS (se genera localmente, no se versiona)
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Instrucciones de ejecución (local)

### 1. Clona el repositorio

```bash
git clone https://github.com/CarlosRW/modova-agente-ia.git
cd modova-agente-ia
```

### 2. Crea y activa un entorno virtual

```bash
python -m venv venv

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configura tu API key de Groq

1. Crea una cuenta gratuita en [Groq Console](https://console.groq.com/keys) y genera una API key.
2. Copia el archivo de ejemplo:
   ```bash
   cp .env.example .env
   ```
3. Pega tu key en `.env`:
   ```
   GROQ_API_KEY=gsk_tu_key_aqui
   ```

### 5. (Opcional) Genera el vectorstore manualmente

```bash
python src/loader.py
```
> Si no lo haces, se genera automáticamente la primera vez que corras el agente.

### 6. Ejecuta el agente

**Por consola:**
```bash
python -m src.agent
```

**Con interfaz web (Streamlit):**
```bash
streamlit run src/app.py
```
Se abrirá en `http://localhost:8501`.

## 💬 Ejemplos de preguntas que el agente puede responder

- ¿Cuántos días tengo para devolver un producto?
- ¿Hacen envíos gratis?
- ¿Qué pasa si mi pedido llega dañado?
- ¿Tienen tienda física?
- ¿Cómo funciona el programa Modova Club?
- ¿Qué métodos de pago aceptan?
- ¿Puedo cancelar mi pedido después de comprarlo?
- ¿Cuánto tardan en darme el reembolso?
- ¿Usan mis datos para publicidad?

## 🧪 Ejemplos de respuestas generadas por el agente

> **Pregunta:** ¿Cuántos días tengo para devolver un producto?
> **Respuesta:** Tienes 30 días calendario desde la fecha de entrega para solicitar una devolución, siempre que el producto esté sin usar, sin lavar y con sus etiquetas originales.

> **Pregunta:** ¿Hacen envíos gratis?
> **Respuesta:** Sí, el envío estándar es gratuito en compras superiores a $80.000. También existe una opción de envío express con costo adicional, con entrega en 24 a 48 horas en ciudades principales.

> **Pregunta:** ¿Qué pasa si mi pedido llega dañado?
> **Respuesta:** Si recibes un producto defectuoso, dañado o diferente al solicitado, Modova cubre el 100% del costo de devolución y puedes elegir entre reembolso total o reemplazo inmediato, sin esperar la inspección del producto devuelto.

> **Pregunta:** ¿Tienen tienda física?
> **Respuesta:** No, Modova opera exclusivamente como tienda online, lo que permite ofrecer precios más competitivos y un catálogo más amplio que una tienda física tradicional.

*(Nota: las respuestas exactas pueden variar levemente entre ejecuciones por la naturaleza generativa del modelo, pero siempre se basan en el contenido real de la documentación.)*

## ☁️ Evidencia del deploy

- **URL pública:** [https://modova-agente-ia.streamlit.app/](https://modova-agente-ia.streamlit.app/)
- **Plataforma:** Streamlit Community Cloud
- Captura de pantalla:

![Agente Modova funcionando](docs/screenshot-deploy.png)

## 📝 Notas de diseño

- Se optó por generar los **embeddings localmente** (en vez de vía API) para evitar dependencias externas de facturación y hacer el proyecto más robusto y reproducible.
- El LLM usa **Groq** por su velocidad de inferencia y generoso tier gratuito.
- El prompt del agente restringe explícitamente al modelo a no inventar información que no esté en el contexto recuperado, derivando al cliente a soporte humano cuando no encuentra la respuesta.

## 👤 Autor

Proyecto desarrollado por CarlosRW como parte del **Challenge Alura Agente** (Oracle Next Education / Alura).
