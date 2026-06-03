import streamlit as st
import os
import httpx
import chromadb
from rank_bm25 import BM25Okapi
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from config import CHROMA_SERVER_URL, DATA_DIR, LMSTUDIO_API_BASE, LLM_MODEL_NAME, EMBEDDING_MODEL_NAME, LMSTUDIO_API_KEY
from ingestion import run_ingestion
from langchain_core.prompts import ChatPromptTemplate

# Create a custom httpx client with a long timeout to prevent [Errno 60] timeouts
custom_client = httpx.Client(timeout=httpx.Timeout(300.0, connect=60.0))

# Initialize Session State at the very top
if "messages" not in st.session_state:
    st.session_state.messages = []
if "retrieval_history" not in st.session_state:
    st.session_state.retrieval_history = []

st.set_page_config(page_title="RAG Lab Dashboard", layout="wide")

st.title("🧪 RAG Lab: Educational Dashboard")
st.markdown("Explore how Retrieval-Augmented Generation works in real-time.")

# Initialize Chroma Client
try:
    client = chromadb.HttpClient(host="localhost", port=8000)
    collection = client.get_or_create_collection(name="rag_lab_collection")
except Exception as e:
    st.error(f"Could not connect to ChromaDB at {CHROMA_SERVER_URL}. Error: {e}")
    collection = None

# Sidebar for configuration status
with st.sidebar:
    st.header("System Status")
    st.success("✅ Python Environment Ready")
    st.info(f"📍 Data Dir: `{DATA_DIR}`")
    st.info(f"🤖 LLM: `{LLM_MODEL_NAME}`")
    
    st.divider()
    if st.button("🗑️ Clear Retrieval History"):
        st.session_state.retrieval_history = []
        st.success("History cleared!")
        st.rerun()

tabs = st.tabs(["📁 Data Ingestion", "🔍 Vector Explorer", "🤖 Chat Lab"])

# --- Tab 1: Data Ingestion ---
with tabs[0]:
    st.header("Ingest Documents")
    st.write("This tab triggers the pipeline to read files from `rag-lab/data`, chunk them, and store vectors in ChromaDB.")
    
    if st.button("🚀 Run Ingestion Pipeline"):
        with st.spinner("Processing documents..."):
            try:
                run_ingestion()
                st.success("Ingestion Complete! Check the Vector Explorer tab.")
            except Exception as e:
                st.error(f"Ingest failed: {e}")
    
    st.subheader("Current Files in Data Directory")
    if os.path.exists(DATA_DIR):
        files = os.listdir(DATA_DIR)
        if files:
            for f in files:
                st.text(f"📄 {f}")
        else:
            st.warning("No files found. Add some .txt, .pdf, .md, .json, .csv, or .html files to `rag-lab/data`!")
    else:
        st.error("Data directory not found.")

# --- Tab 2: Vector Explorer ---
with tabs[1]:
    st.header("Explore the Vector Database")
    st.write("Browse through the chunks that have been embedded and stored in ChromaDB.")
    
    if collection is not None:
        try:
            count = collection.count()
            st.metric("Total Chunks Stored", count)
            
            if count > 0:
                items = collection.get(limit=20)
                for i in range(len(items['ids'])):
                    with st.expander(f"Chunk ID: {items['ids'][i]}"):
                        st.write("**Content:**")
                        st.text_area("Text", items['documents'][i], height=150, key=int(i), label_visibility="collapsed")
                        st.write("**Metadata:**")
                        st.json(items['metadatas'][i])
            else:
                st.info("The collection is empty. Run ingestion first!")
        except Exception as e:
            st.error(f"Error fetching from ChromaDB: {e}")
    else:
        st.warning("ChromaDB connection unavailable.")

# --- Tab 3: Chat Lab ---
with tabs[2]:
    st.header("RAG Chat Interface")
    st.write("Ask a question about your documents. The system will retrieve relevant context and use LMStudio to answer.")

    if collection is None:
        st.error("ChromaDB connection unavailable. Please check your Podman container.")
    else:
        try:
            embeddings = OpenAIEmbeddings(
                openai_api_base=LMSTUDIO_API_BASE,
                openai_api_key=LMSTUDIO_API_KEY,
                check_embedding_ctx_length=False,
                http_client=custom_client
            )
            llm = ChatOpenAI(
                openai_api_base=LMSTUDIO_API_BASE,
                openai_api_key=LMSTUDIO_API_KEY,
                model=LLM_MODEL_NAME,
                temperature=0,
                http_client=custom_client
            )
        except Exception as e:
            st.error(f"Error initializing AI components: {e}")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        with st.expander("⚙️ Retrieval Settings", expanded=True):
            k_value = st.number_input("Number of chunks to retrieve (k)", min_value=1, max_value=20, value=3)
            similarity_threshold = st.slider("Similarity Threshold", min_value=0.0, max_value=1.0, value=0.0, step=0.05)
            use_hybrid_search = st.checkbox("Enable Hybrid Search (BM25 + Vector)", value=False)

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask something about your documents..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Searching for context and generating answer..."):
                    try:
                        vectorstore = Chroma(
                            client=client,
                            collection_name="rag_lab_collection",
                            embedding_function=embeddings
                        )

                        results = vectorstore.similarity_search_with_score(prompt, k=k_value)
                        
                        docs = []
                        scores = []
                        for doc, score in results:
                            sim_score = 1.0 - score
                            if sim_score >= similarity_threshold:
                                docs.append(doc)
                                scores.append(sim_score)
                        
                        context_text = "\n\n".join([d.page_content for d in docs])
                        
                        st.session_state.retrieval_history.insert(0, {
                            "query": prompt,
                            "context": context_text,
                            "scores": scores,
                            "docs": docs
                        })

                        system_prompt = f"""You are a helpful assistant. Use the following pieces of retrieved context to answer the user's question. 
                        If you don't know the answer based on the context, just say that you don't know. 
                        Context:
                        {context_text}"""
                        
                        chat_prompt = ChatPromptTemplate.from_messages([
                            ("system", system_prompt),
                            ("human", "{input}")
                        ])
                        
                        chain = chat_prompt | llm
                        response = chain.invoke({"input": prompt})
                        full_response = response.content

                        st.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                    except Exception as e:
                        error_msg = f"Error during RAG process: {e}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})

        if st.session_state.retrieval_history:
            st.subheader("📜 Retrieval History")
            for idx, history in enumerate(st.session_state.retrieval_history):
                with st.expander(f"Query: {history['query'][:50]}... (Index: {idx})"):
                    if not history['docs']:
                        st.warning("No chunks met the similarity threshold for this query.")
                    else:
                        for i, doc in enumerate(history['docs']):
                            st.markdown(f"**Chunk {i+1} (Similarity: {history['scores'][i]:.4F})**")
                            st.write(doc.page_content)
                            st.divider()
                    st.caption(f"Retrieved {len(history['docs'])} chunks for this query.")
        else:
            st.info("No retrieval history available. Start a chat to see results here!")
