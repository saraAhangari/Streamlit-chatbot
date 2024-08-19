import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from llama_index.core import Document, VectorStoreIndex
from database import query_user_data
from web_crawler import crawl_websites
from utils import split_text, generate_embeddings, store_embeddings, retrieve_top_k_chunks
import chromadb

system_prompt = """
    You are a helpful assistant for BluBank. Your role is to answer questions by providing 
    information about BluBank services and user-specific account details, if available. 
    When a user asks about the services you can offer, inform them that you can provide 
    information about BluBank and any personal account they may have, as long as it adheres 
    to the bank's guidelines. For every question, you should check both the database and available 
    web sources to give the most accurate and relevant answer. If a question is not relevant to the data 
    you have or if for any reason you cannot answer, politely apologize and inform the user that they
    will be connected to an expert. Always respond in the language the user is speaking, and if the user
    switches languages, adapt your response to match their language.
"""

def extract_account_number(prompt: str) -> str:
    """
    Extract an account number from the user's prompt.

    Args:
        prompt (str): The user's input string.

    Returns:
        str: Extracted account number if found, otherwise None.
    """
    import re
    match = re.search(r'\b\d{5}\b', prompt)  
    return match.group(0) if match else None

def generate_personalized_response(user_data: dict) -> str:
    """
    Generate a personalized response in Persian based on the user's data.

    Args:
        user_data (dict): Dictionary containing user's account details.

    Returns:
        str: Personalized response text in Persian.
    """
    response = f"بر اساس اطلاعات حساب شما، {user_data['customer_name']}، می‌توانم به شما بگویم: \n"
    response += f"گردش حساب: {user_data['turnover']} \n"
    return response

def search_content(prompt: str, content: str) -> str:
    """
    Search the provided content for information relevant to the user's prompt and return the response as a string.

    Args:
        prompt (str): The user's query or input.
        content (str): The textual content to search within for relevant information.

    Returns:
        str: The generated response based on the search, returned as a string.
    """
    document = Document(text=content)
    index = VectorStoreIndex.from_documents([document])
    query_engine = index.as_query_engine(streaming=True)
    streaming_response = query_engine.query(prompt)
    response_gen = streaming_response.response_gen
    return st.write_stream(response_gen)

def process_prompt(prompt: str, urls: list, engine) -> str:
    """
    Process the user's prompt to generate an appropriate response by checking the database and crawling websites.

    Args:
        prompt (str): The user's input string.
        urls (list): List of URLs to crawl for information.
        engine (Engine): SQLAlchemy Engine object for database interaction.

    Returns:
        str: Generated response text.
    """
    account_number = extract_account_number(prompt)
    if account_number:
        user_data = query_user_data(engine, account_number)
        if user_data:
            return generate_personalized_response(user_data)
        else:
            return "Sorry, your account number is not valid."

    web_content = crawl_websites(urls)
    text_chunks = split_text(web_content)
    embeddings = generate_embeddings(text_chunks)
    client = chromadb.Client()
    collection = client.create_collection("web_content")
    store_embeddings(embeddings, text_chunks, collection)
    query_embedding = generate_embeddings([prompt])[0]
    top_k_chunks = retrieve_top_k_chunks(query_embedding, collection)
    selected_chunks = "\n".join(top_k_chunks)
    return search_content(prompt, selected_chunks)
