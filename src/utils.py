import os
import streamlit as st
import toml
from openai import OpenAI
import chromadb

SECRETS_PATH = os.path.join("./.streamlit", "secrets.toml")

def load_secrets() -> dict:
    """
    Load secrets from the TOML file.

    Returns:
        dict: Dictionary containing the loaded secrets.
    """
    return toml.load(SECRETS_PATH)

def setup_session_variables() -> None:
    """
    Initialize session variables if they are not already set.

    Returns:
        None
    """
    st.session_state.setdefault("openai_model", "gpt-4")
    st.session_state.setdefault("messages", [])

def display_messages() -> None:
    """
    Display chat messages stored in the session state.

    Returns:
        None
    """
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """
    Split text into chunks of a specified size with an overlap.

    Args:
        text (str): The text to split.
        chunk_size (int, optional): The size of each chunk. Defaults to 500.
        overlap (int, optional): The overlap between chunks. Defaults to 50.

    Returns:
        list: List of text chunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def generate_embeddings(text_chunks: list, model="text-embedding-ada-002") -> list:
    """
    Generate embeddings for a list of text chunks using the OpenAI API.

    Args:
        text_chunks (list): List of text chunks to generate embeddings for.
        model (str, optional): The model to use for generating embeddings. Defaults to "text-embedding-ada-002".

    Returns:
        list: List of generated embeddings.
    """
    secrets = load_secrets()
    client = OpenAI(api_key=secrets.get("OPENAI_API_KEY"))
    embeddings = []
    for chunk in text_chunks:
        response = client.embeddings.create(model=model, input=[chunk])
        embeddings.append(response.data[0].embedding)
    return embeddings

def store_embeddings(embeddings: list, text_chunks: list, collection) -> None:
    """
    Store embeddings in ChromaDB.

    Args:
        embeddings (list): List of embeddings to store.
        text_chunks (list): List of text chunks corresponding to the embeddings.
        collection: The ChromaDB collection to store the embeddings in.

    Returns:
        None
    """
    for i, embedding in enumerate(embeddings):
        collection.add(embeddings=[embedding], metadatas=[{"text": text_chunks[i]}], ids=[str(i)])

def retrieve_top_k_chunks(query_embedding: list, collection, k: int = 5) -> list:
    """
    Retrieve the top-k most similar chunks based on the query embedding.

    Args:
        query_embedding (list): The embedding of the query to match against.
        collection: The ChromaDB collection containing the stored embeddings.
        k (int, optional): The number of top chunks to retrieve. Defaults to 5.

    Returns:
        list: List of top-k chunks' text.
    """
    results = collection.query(query_embeddings=[query_embedding], n_results=k)
    return [result["text"] for result in results["metadatas"][0]]
