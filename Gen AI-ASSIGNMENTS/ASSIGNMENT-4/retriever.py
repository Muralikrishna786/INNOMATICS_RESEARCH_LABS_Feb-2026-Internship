from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, PERSIST_DIR


# -----------------------------
# Embeddings
# -----------------------------
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )


# -----------------------------
# Retriever
# -----------------------------
def get_retriever():
    embeddings = get_embeddings()

    vectordb = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

    # ✅ Use MMR for better results (avoids duplicate chunks)
    return vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 4,
            "fetch_k": 8
        }
    )


# -----------------------------
# LLM
# -----------------------------
def get_llm():
    if not OPENAI_API_KEY:
        raise ValueError("❌ OPENAI_API_KEY not found in .env file")

    return ChatOpenAI(
        temperature=0,
        api_key=OPENAI_API_KEY
    )