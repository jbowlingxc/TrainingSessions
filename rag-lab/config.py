import os

# LMStudio Configuration
LMSTUDIO_API_BASE = "http://172.16.103.72:1234/v1"
# LMSTUDIO_API_KEY = os.getenv("LMSTUDIO_API_KEY", "lm-studio")
LMSTUDIO_API_KEY = "sk-lm-ji3g3ljO:wvNsLUlWCFNqyvK5dbet"
EMBEDDING_MODEL_NAME = "text-embedding-nomic-embed-text-v1.5@q8_0"
LLM_MODEL_NAME = "meta-llama-3.1-8b-instruct"

# ChromaDB Configuration
# Since we are running Chroma in a Podman container, we connect via HTTP
CHROMA_HOST = "localhost"
CHROMA_PORT = 8000
CHROMA_SERVER_URL = f"http://{CHROMA_HOST}:{CHROMA_PORT}"

# Data Configuration
DATA_DIR = "data"

VECTOR_DB_DIR = ".chroma_db" # For local persistence if needed, but we use server
