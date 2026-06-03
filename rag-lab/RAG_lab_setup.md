# RAG Lab Setup Guide

This guide provides step-by-step instructions to set up an educational Retrieval-Augmented Generation (RAG) laboratory. This lab demonstrates how unstructured data is transformed into searchable vectors and used to augment LLM responses using **ChromaDB** for storage and **LMStudio** for local inference.

## 🛠 Prerequisites

Before starting, ensure you have the following installed:
- [Podman](https://podman.io/) (for running ChromaDB)
- [LMStudio](https://lmstudio.ai/) (for local LLM/Embedding inference)
- [uv](https://github.com/astray-sh/uv) (for extremely fast Python package and environment management)
- Python 3.10+
- Git

## 🧐 Rationale for Tool Selection

To build an effective educational lab, we have selected tools that balance performance, ease of use, and transparency.

*   **Podman & ChromaDB**: We use **Podman** to run **ChromaDB** because it provides a clean, isolated environment without the overhead of a full virtual machine. ChromaDB is chosen for its lightweight, developer-friendly nature and excellent support for local vector storage.
*   **LMStudio**: This acts as our orchestration layer for models. It provides an **OpenAI-compatible API**, which allows us to use standard libraries like `langchain` without complex custom networking logic.
*   **nomic-embed-text-v1.5**: This embedding model is specifically optimized for high-performance retrieval and has a large context window, making it ideal for demonstrating how text chunks are mapped to vectors.
*   **Meta-Llama-3-8B-Instruct-GGUF_Q8_0**: 
    *   **Instruction-Tuned**: In RAG, the model must follow a specific instruction: *"Answer the question using only the provided context."* A base model might simply continue the text, whereas an **instruction-tuned** model is trained to adhere to these structural constraints and handle "I don't know" scenarios when context is missing.
    *   **GGUF Format**: The GGUF format allows us to run powerful models on consumer-grade hardware via LMStudio with minimal memory footprint.

---

We will run ChromaDB as a persistent service using Podman to keep the host environment clean.

1. **Pull and Run ChromaDB**:
   Execute the following command to start the ChromaDB server container.
   ```bash
   podman run -d \
     --name rag-chromadb \
     -p 8000:8000 \
     chromadb/chroma
   ```

2. **Verify Container**:
   Ensure the container is running:
   ```bash
   podman ps
   ```

---

## 🧠 Step 2: Inference Server Setup (LMStudio)

LMStudio will act as our local OpenAI-compatible API for both embeddings and text generation.

1. **Download Embedding Model**:
   Open LMStudio and search for/download: `nomic-ai/nomic-embed-text-v1.5-GGUF`. This model is highly efficient for retrieval tasks.
2. **Download LLM Model**:
   Download a capable instruction-tuned model (e.g., `Meta-Llama-3-8B-Instruct-GGUF`). Use a Q8 model if possible.
3. **Start Local Server**:
   - Go to the **Local Server** tab in LMStudio.
   - Load both the Embedding and Chat models.
   - Ensure the server is started on `http://localhost:1234`.

---



## 🐍 Step 3: Python Environment Setup

We will use **`uv`** for lightning-fast environment and dependency management.

1. **Create and Activate Virtual Environment**:
   ```bash
   cd rag-lab
   uv venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   uv pip install langchain langchain-community chromadb openai streamlit pypdf langchain-openai langchain-text-splitters rank-bm25
   ```

---



## 🚀 Step 4: Implementation Roadmap

This next section describes custom scripts that you will use. It consists of three primary Python modules that you will implement:

### 1. `config.py`
Defines the connection strings for LMStudio (`http://localhost:1234/v1`) and ChromaDB.

### 2. `ingestion.py` (The "How it Works" Module)
This script will:
- Load PDFs/Text files from a local `./data` folder.
- Split text into chunks using `RecursiveCharacterTextSplitter`.
- Use LMStudio's embedding model to vectorize chunks.
- Store vectors and metadata in the ChromaDB container.

### 3. `app.py` (The Educational Dashboard)
A **Streamlit** application featuring:
- **Data Ingestion Tab**: Trigger the ingestion process and view chunking previews.
- **Vector Explorer Tab**: Browse stored documents and their associated metadata.
- **Chat Lab Tab**: An interactive chat interface that shows the "Retrieved Context" used for every response, making the RAG process transparent.

---

## 📂 Project Structure

```text
rag-lab/
├── data/               # Place your source PDFs/TXTs here
├── .venv/              # Python virtual environment
├── config.py           # Configuration & API endpoints
├── ingestion.py        # Processing & Embedding logic
├── app.py              # Streamlit UI
└── requirements.txt    # Project dependencies
```

## 🏁 Running the Lab

Once all modules are implemented:
1. Ensure the **Podman** container is running.
2. Ensure **LMStudio** server is active.
3. Launch the dashboard:
   ```bash
   streamlit run app.py
   ```

2. **Verify Container**:
   Ensure the container is running:
   ```bash
   podman ps
   ```

---

## 🧠 Step 2: Inference Server Setup (LMStudio)

LMStudio will act as our local OpenAI-compatible API for both embeddings and text generation.

1. **Download Embedding Model**:
   Open LMStudio and search for/download: `nomic-ai/nomic-embed-text-v1.5-GGUF`. This model is highly efficient for retrieval tasks.
2. **Download LLM Model**:
   Download a capable instruction-tuned model (e.g., `Meta-Llama-3-8B-Instruct-GGUF`). Use a Q8 model if possible.
3. **Start Local Server**:
   - Go to the **Local Server** tab in LMStudio.
   - Load both the Embedding and Chat models.
   - Ensure the server is started on `http://localhost:1234`.

---

## 🐍 Step 3: Python Environment Setup

We will use **`uv`** for lightning-fast environment and dependency management.

1. **Create and Activate Virtual Environment**:
   ```bash
   cd project-directory
   uv venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   uv pip install langchain langchain-community chromadb openai streamlit pypdf langchain-openai langchain-text-splitters
   ```

---

## 🚀 Step 4: Implementation Roadmap

This next section describes custom scripts that you will use. It consists of three primary Python modules that you will implement:

### 1. `config.py`
Defines the connection strings for LMStudio (`http://localhost:1234/v1`) and ChromaDB.

### 2. `ingestion.py` (The "How it Works" Module)
This script will:
- Load PDFs/Text files from a local `./data` folder.
- Split text into chunks using `RecursiveCharacterTextSplitter`.
- Use LMStudio's embedding model to vectorize chunks.
- Store vectors and metadata in the ChromaDB container.

### 3. `app.py` (The Educational Dashboard)
A **Streamlit** application featuring:
- **Data Ingestion Tab**: Trigger the ingestion process and view chunking previews.
- **Vector Explorer Tab**: Browse stored documents and their associated metadata.
- **Chat Lab Tab**: An interactive chat interface that shows the "Retrieved Context" used for every response, making the RAG process transparent.

---

## 📂 Project Structure

```text
rag-lab/
├── data/               # Place your source PDFs/TXTs here
├── venv/               # Python virtual environment
├── config.py           # Configuration & API endpoints
├── ingestion.py        # Processing & Embedding logic
├── app.py              # Streamlit UI
└── requirements.txt    # Project dependencies
```

## 🏁 Running the Lab

Once all modules are implemented:
1. Ensure the **Podman** container is running.
2. Ensure **LMStudio** server is active.
3. Launch the dashboard:
   ```bash
   streamlit run app.py
   ```
