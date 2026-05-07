# RAG Document Assistant

API REST desarrollada en Python para realizar preguntas sobre documentos utilizando una arquitectura RAG (*Retrieval-Augmented Generation*).

El sistema permite subir documentos en formato PDF o TXT, extraer su contenido, dividirlo en fragmentos, generar embeddings con Gemini, almacenarlos en una base vectorial con ChromaDB y responder preguntas utilizando únicamente el contexto recuperado de los documentos.

Este proyecto está orientado a practicar conceptos de IA generativa aplicada, RAG, embeddings, búsqueda semántica, APIs REST y uso de modelos LLM mediante API.

---

## Objetivo del proyecto

El objetivo principal es construir una aplicación sencilla pero funcional que permita consultar documentos mediante lenguaje natural.

A diferencia de una llamada directa a un LLM, este sistema no responde únicamente con el conocimiento interno del modelo. Primero recupera fragmentos relevantes del documento y después genera una respuesta basada en ese contexto.

El flujo general es:

```text
Documento PDF/TXT
     ↓
Extracción de texto
     ↓
División en chunks
     ↓
Embeddings con Gemini
     ↓
Almacenamiento en ChromaDB
     ↓
Pregunta del usuario
     ↓
Búsqueda semántica
     ↓
Respuesta generada con Gemini usando el contexto recuperado
```

---

## Tecnologías utilizadas

- Python
- FastAPI
- Pydantic
- Uvicorn
- Gemini API
- Gemini Embeddings
- ChromaDB
- pypdf
- python-dotenv
- pytest

---

## Estructura del proyecto

```text
rag-document-assistant/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   ├── config.py
│   ├── document_loader.py
│   ├── text_splitter.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retrieval.py
│   ├── retrieval_utils.py
│   ├── rag_chain.py
│   └── llm_client.py
│
├── data/
│   ├── uploads/
│   └── chroma/
│
├── examples/
│   └── sample_question.json
│
├── tests/
│   ├── test_text_splitter.py
│   └── test_retrieval.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Funcionamiento general

El sistema se divide en dos fases principales.

### 1. Indexación de documentos

Cuando se sube un documento, la API realiza los siguientes pasos:

```text
Archivo PDF/TXT
     ↓
Extracción del texto
     ↓
División en fragmentos
     ↓
Generación de embeddings
     ↓
Almacenamiento en ChromaDB
```

Cada fragmento queda guardado junto con su documento de origen y un identificador de chunk.

### 2. Pregunta y respuesta

Cuando el usuario realiza una pregunta:

```text
Pregunta del usuario
     ↓
Embedding de la pregunta
     ↓
Búsqueda de chunks similares en ChromaDB
     ↓
Construcción del contexto
     ↓
Llamada a Gemini
     ↓
Respuesta final con fuentes
```

La respuesta incluye tanto el texto generado como los fragmentos utilizados como fuente.

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/mairena8m/rag-document-assistant.git
cd rag-document-assistant
```

### 2. Crear entorno virtual

En Windows CMD:

```bash
python -m venv venv
venv\Scripts\activate
```

En Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

En Linux/Mac:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Configuración

Crea un archivo `.env` en la raíz del proyecto.

Puedes basarte en el archivo `.env.example`:

```env
GEMINI_API_KEY=tu_api_key_aqui
GEMINI_GENERATION_MODEL=gemini-2.5-flash-lite
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
CHROMA_PATH=data/chroma
UPLOADS_PATH=data/uploads
```

Importante: el archivo `.env` no debe subirse nunca a GitHub porque contiene claves privadas.

---

## Ejecutar la API

Desde la raíz del proyecto:

```bash
python -m uvicorn app.main:app --reload
```

Después, abre en el navegador:

```text
http://127.0.0.1:8000/docs
```

FastAPI mostrará una interfaz interactiva donde se pueden probar los endpoints.

---

## Endpoints disponibles

### Health check

```http
GET /health
```

Respuesta esperada:

```json
{
  "status": "ok"
}
```

---

### Subir documento

```http
POST /documents/upload
```

Permite subir un archivo PDF o TXT.

El sistema extrae el texto, lo divide en chunks, genera embeddings y guarda la información en ChromaDB.

Ejemplo de respuesta:

```json
{
  "document_name": "TFG_Memoria.pdf",
  "chunks_created": 80,
  "status": "indexed"
}
```

---

### Hacer una pregunta

```http
POST /ask
```

Ejemplo de entrada:

```json
{
  "question": "¿Qué modelo obtuvo el mejor resultado?",
  "top_k": 4
}
```

Ejemplo de respuesta:

```json
{
  "answer": "El modelo U-Net++ obtuvo el mejor resultado global.",
  "sources": [
    {
      "document_name": "TFG_Memoria.pdf",
      "chunk_id": "TFG_Memoria.pdf_60_1b6a0f93",
      "text": "Tabla 3.8: Comparación de métricas para los modelos de segmentación...",
      "distance": 0.5306985974311829
    }
  ]
}
```

La respuesta final se genera con Gemini a partir de los fragmentos recuperados del documento.

---

### Buscar chunks relevantes

```http
POST /retrieval/search
```

Este endpoint permite ver qué fragmentos recupera el sistema antes de generar una respuesta con Gemini.

Sirve para depurar el comportamiento del RAG y comprobar si la búsqueda semántica está recuperando contexto útil.

Ejemplo de entrada:

```json
{
  "question": "¿Qué modelo obtuvo el mejor resultado?",
  "top_k": 4
}
```

Ejemplo de respuesta:

```json
{
  "query": "¿Qué modelo obtuvo el mejor resultado?",
  "results": [
    {
      "document_name": "TFG_Memoria.pdf",
      "chunk_id": "TFG_Memoria.pdf_60_1b6a0f93",
      "text": "El modelo U-Net++ se posiciona como la arquitectura con mejor desempeño global...",
      "distance": 0.5306985974311829
    },
    {
      "document_name": "TFG_Memoria.pdf",
      "chunk_id": "TFG_Memoria.pdf_64_a87ded3b",
      "text": "Tras la revisión, apuntó que U-Net++, FPN y PSPNet fueron los modelos que mejor trabajo desempeñaban...",
      "distance": 0.5459016561508179
    }
  ]
}
```

La distancia permite analizar la relevancia de los fragmentos recuperados. En general, una distancia menor indica mayor similitud entre la pregunta y el fragmento.

---

### Listar documentos indexados

```http
GET /documents
```

Ejemplo de respuesta:

```json
{
  "documents": [
    "TFG_Memoria.pdf"
  ]
}
```

---

### Reiniciar colección vectorial

```http
DELETE /documents/reset
```

Elimina la colección actual de ChromaDB y crea una nueva.

Ejemplo de respuesta:

```json
{
  "status": "collection reset"
}
```

---

## Ejemplo usando PowerShell

Una vez arrancada la API, se puede hacer una pregunta así:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/ask" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"question": "¿Qué modelo obtuvo el mejor resultado?", "top_k": 4}'
```

También se puede comprobar la recuperación de chunks sin generar respuesta final:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/retrieval/search" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"question": "¿Qué modelo obtuvo el mejor resultado?", "top_k": 4}'
```

---

## Tests

El proyecto incluye tests unitarios para comprobar partes internas del sistema.

Para ejecutar los tests:

```bash
python -m pytest -v
```

Actualmente se validan aspectos como:

- División de texto en chunks.
- Comportamiento ante texto vacío.
- Control de errores cuando `chunk_size` no es válido.
- Control de errores cuando `overlap` es mayor o igual que `chunk_size`.
- Filtrado de chunks por distancia.
- Comportamiento del filtro cuando no hay chunks.
- Comportamiento del filtro cuando no hay distancia disponible.

Los tests se centran en la lógica interna y no dependen directamente de Gemini ni de ChromaDB, para evitar que fallen por servicios externos o límites de cuota.

---

## Limitaciones

Este proyecto es una versión inicial funcional y no debe considerarse un sistema RAG avanzado.

Limitaciones principales:

- La extracción de texto desde PDF puede generar texto con espacios incorrectos o ruido.
- La división en chunks es básica y no tiene en cuenta estructura semántica avanzada.
- La calidad de la respuesta depende de la calidad de los chunks recuperados.
- Si se usan documentos grandes con el free tier de Gemini, pueden aparecer errores de cuota o rate limit durante la generación de embeddings.
- La base vectorial se almacena localmente en `data/chroma`.
- No incluye autenticación ni control de usuarios.
- No filtra de forma avanzada todos los fragmentos poco informativos.
- Las distancias de recuperación ayudan a depurar, pero no sustituyen una evaluación formal de calidad del RAG.
- No incluye evaluación automática de fidelidad, alucinaciones o calidad de respuesta.

---

## Posibles mejoras futuras

- Añadir limpieza avanzada del texto extraído de PDF.
- Añadir filtrado más robusto de chunks poco relevantes.
- Ajustar dinámicamente el número de chunks utilizados según la distancia.
- Añadir soporte para documentos DOCX.
- Añadir carga múltiple de documentos.
- Añadir una interfaz web sencilla.
- Añadir Dockerfile para facilitar el despliegue.
- Añadir evaluación básica de respuestas RAG.
- Añadir soporte para embeddings locales para evitar límites de cuota.
- Añadir autenticación para proteger los endpoints.
- Añadir tests de integración con documentos de ejemplo.

---

## Estado del proyecto

Versión inicial funcional.

El proyecto permite subir documentos PDF o TXT, generar embeddings, almacenarlos en ChromaDB y realizar preguntas sobre el contenido mediante una arquitectura RAG con Gemini.

También incluye un endpoint de depuración para inspeccionar los fragmentos recuperados antes de generar la respuesta final.