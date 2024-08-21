import os
import sys

import chromadb
import pandas as pd
from openai import OpenAI

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from utils import load_secrets
from web_crawler import crawl_websites


def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """
    Split text into chunks of a specified size with an overlap.

    Args:
        text (str): The text to split.
        chunk_size (int, optional): The size of each chunk. Defaults to 500.
        overlap (int, optional): The overlap between chunks. Defaults to 50.

    Returns:
        list: List of tuples containing the chunk and its index.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append((chunk, start // (chunk_size - overlap))) 
        start += chunk_size - overlap
    return chunks

def store_embeddings(embeddings_with_indices: list, collection) -> None:
    """
    Store embeddings in ChromaDB along with their indices.

    Args:
        embeddings_with_indices (list): A list of tuples containing embeddings and their corresponding chunk indices.
        collection: The ChromaDB collection to store the embeddings in.

    Returns:
        None
    """
    for embedding, index in embeddings_with_indices:
        collection.add(embeddings=[embedding], metadatas=[{"index": index}], ids=[str(index)])

def retrieve_top_k_chunks(query_embedding: list, collection, k: int = 5) -> list:
    """
    Retrieve the top-k most similar chunks based on the query embedding.

    Args:
        query_embedding (list): The embedding of the query to match against.
        collection: The ChromaDB collection containing the stored embeddings.
        k (int, optional): The number of top chunks to retrieve. Defaults to 5.

    Returns:
        list: A list of tuples containing the chunk content and its index.
    """
    results = collection.query(query_embeddings=[query_embedding], n_results=k)
    top_k_indices = [result["index"] for result in results["metadatas"][0]]
    return top_k_indices        


def generate_embedding_for_chunk(chunk: str, model="text-embedding-ada-002") -> list:
    """
    Generate an embedding for a given chunk of text using OpenAI's API.

    Args:
        chunk (str): The text chunk to generate an embedding for.
        model (str, optional): The embedding model to use. Defaults to "text-embedding-ada-002".

    Returns:
        list: The embedding vector for the chunk.
    """
    secrets = load_secrets()
    client = OpenAI(api_key=secrets.get("OPENAI_API_KEY"))
    
    response = client.embeddings.create(input=[chunk], model=model)
    embedding = response.data[0].embedding 
    
    return embedding

def generate_embeddings_with_indices(text_chunks: list, model="text-embedding-ada-002") -> list:
    """
    Generate embeddings for a list of text chunks and return the embeddings along with their indices.

    Args:
        text_chunks (list): A list of tuples where each tuple contains a chunk and its corresponding index.
        model (str, optional): The embedding model to use. Defaults to "text-embedding-ada-002".

    Returns:
        list: A list of tuples where each tuple contains the embedding and the corresponding chunk index.
    """
    embeddings_with_indices = []

    for chunk, index in text_chunks:
        embedding = generate_embedding_for_chunk(chunk, model=model)
        embeddings_with_indices.append((embedding, index))
    
    return embeddings_with_indices

def get_top_chunks(questions: list, urls: list, k: int = 5) -> pd.DataFrame:
    """
    Process a list of questions, retrieve the top-k chunks for each, and return a DataFrame.

    Args:
        questions (list): List of questions to process.
        urls (list): List of URLs to crawl for generating text chunks.
        k (int, optional): The number of top chunks to retrieve. Defaults to 5.

    Returns:
        pd.DataFrame: DataFrame containing the question and the indices of selected chunks.
    """

    web_content = crawl_websites(urls)
    
    text_chunks_with_indices = split_text(web_content)
    
    embeddings_with_indices = generate_embeddings_with_indices(text_chunks_with_indices)
    
    client = chromadb.Client()
    collection = client.get_or_create_collection("web_content")
    store_embeddings(embeddings_with_indices, collection)
    

    df = pd.DataFrame(columns=["question", "top_k_chunks"])
    
    for question in questions:
        query_embedding = generate_embedding_for_chunk(question) 
        top_k_indices = retrieve_top_k_chunks(query_embedding, collection, k=k)
        
        new_row = pd.DataFrame([{
            "question": question,
            "top_k_chunks": top_k_indices
        }])
        
        df = pd.concat([df, new_row], ignore_index=True)
    
    return df

if __name__ == "__main__":
    secrets = load_secrets()
    urls = secrets['CRAWLER_URLS']
    
    questions = [
        "چگونه می‌توان از بلوبانک وام دریافت کرد؟",
        "حداقل میانگین حساب برای دریافت وام از بلوبانک چقدر است؟",
        "سقف وام‌های بلوبانک چقدر است؟",
        "مدت زمان بازپرداخت وام‌های بلوبانک چقدر است؟",
        "آیا برای دریافت وام از بلوبانک نیاز به ضامن است؟",
        "چه نوع وثیقه‌ای برای دریافت وام از بلوبانک نیاز است؟",
        "چگونه می‌توان اعتبارسنجی خود را در بلوبانک بهبود داد؟",
        "آیا امکان دریافت وام بدون داشتن حساب فعال در بلوبانک وجود دارد؟",
        "فرآیند درخواست وام از بلوبانک چگونه است؟",
        "چگونه می‌توان وضعیت درخواست وام را در بلوبانک پیگیری کرد؟",
        "آیا بلوبانک نرخ بهره مشخصی برای وام‌ها دارد؟",
        "آیا امکان تغییر شرایط بازپرداخت وام در بلوبانک وجود دارد؟",
        "آیا بلوبانک وام‌های بلندمدت ارائه می‌دهد؟",
        "چه مدارکی برای درخواست وام در بلوبانک نیاز است؟",
        "چگونه می‌توان از پیشنهادات ویژه وام‌های بلوبانک مطلع شد؟",
        "آیا امکان دریافت وام دوم از بلوبانک پس از بازپرداخت وام اول وجود دارد؟",
        "آیا بلوبانک برای دانشجویان نیز وام ارائه می‌دهد؟",
        "چه عواملی می‌توانند باعث رد شدن درخواست وام در بلوبانک شوند؟",
        "آیا بلوبانک طرح‌های تشویقی برای مشتریان وام‌گیرنده دارد؟",
        "چگونه می‌توان از خدمات پشتیبانی بلوبانک در مورد وام‌ها استفاده کرد؟"
    ]
    
    df = get_top_chunks(questions, urls)
    df.to_csv('Evaluation/Retrieve/Files/selected_chunks.csv', index=False)
