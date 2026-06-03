import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb
from config import CHROMA_SERVER_URL, DATA_DIR, LMSTUDIO_API_BASE, EMBEDDING_MODEL_NAME, LMSTUDIO_API_KEY

def run_ingestion():
    # 1. Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        print(f"Error: Data directory '{DATA_DIR}' not and path issue...") # Placeholder error logic
        # Let's make it more robust
        os.makedirs(DATA_DIR, exist_ok=True)

    print(f"Starting ingestion from {DATA_DIR}...")

    # 2. Load Documents
    # We support PDF and Text files for this lab
    documents = []
    for file in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, file)
        ext = os.path.splitext(file)[1].lower()
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
        elif ext in [".txt", ".md", ".json", ".html"]:
            loader = TextLoader(file_path, encoding="utf-8")
            documents.extend(loader.load())
        elif ext == ".csv":
            loader = CSVLoader(file_path)
            documents.extend(loader.load())


    if not documents:
        print("No documents found to ingest in rag-lab/data. Please add some .txt, .pdf, .md, .json, .csv, or .html files.")
        return

    # 3. Split Documents into Chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split documents into {len(chunks)} chunks.")

    # 4. Initialize Embeddings (LMStudio)
    embeddings = OpenAIEmbeddings(
        openai_api_base=LMSTUDIO_API_BASE,
        openai_api_key=LMSTUDIO_API_KEY, 
        check_embedding_ctx_length=False 
    )

    # 5. Connect to ChromaDB (via HttpClient)
    client = chromadb.HttpClient(host="localhost", port=8000)
    
    # 6. Create Vector Store and Add Chunks
    print("Adding chunks to ChromaDB...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        client=client,
        collection_name="rag_lab_collection"
    )

    print("Ingestion complete!")

if __name__ == "__main__":
    run_ingestion()

