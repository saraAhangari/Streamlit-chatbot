import os
import streamlit as st
from llama_index.core import VectorStoreIndex, Document
from PIL import Image
import toml
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage

# Load secrets
secrets_path = os.path.join(".streamlit", "secrets.toml")
secrets = toml.load(secrets_path)

urls = secrets['CRAWLER_URLS']

# Initialize ChatMessageHistory
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = ChatMessageHistory()

# Database connection
def get_postgres_connection():
    postgres_config = secrets['postgres']
    engine = create_engine(f"postgresql://{postgres_config['user']}:{postgres_config['password']}@{postgres_config['host']}:{postgres_config['port']}/{postgres_config['dbname']}")
    return engine

# Extract account number
def extract_account_number(prompt):
    import re
    match = re.search(r'\b\d{5}\b', prompt)  
    if match:
        return match.group(0)
    return None

# Query user data
def query_user_data(account_number):
    engine = get_postgres_connection()
    query = text("SELECT turnover, customer_name FROM facts.account_turnover WHERE account_no = :account_number")
    with engine.connect() as connection:
        result = connection.execute(query, {'account_number': int(account_number)})
        user_data = result.fetchone()  
        
        if user_data:
            return {'turnover': user_data[0], 'customer_name': user_data[1]}
        else:
            return None

# Generate personalized response
def generate_personalized_response(user_data):
    response = f"Based on your account information, {user_data['customer_name']}, here's what I can tell you: \n"
    response += f"Account turnover: {user_data['turnover']} \n"
    return response

# Crawl webpage
def crawl_webpage(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text(separator=' ')
    except Exception as e:
        st.error(f"Error crawling {url}: {str(e)}")
        return ""

# Crawl multiple websites
def crawl_websites(urls):
    content = ""
    for url in urls:
        content += crawl_webpage(url)
    return content

# Search content function
def search_content(prompt, content):
    document = Document(text=content)
    index = VectorStoreIndex.from_documents([document])
    query_engine = index.as_query_engine(streaming=True)
    streaming_response = query_engine.query(prompt)
    response_gen = streaming_response.response_gen
    return st.write_stream(response_gen)

# Process prompt
def process_prompt(prompt, urls):
    account_number = extract_account_number(prompt)
    
    # Append user message to chat history
    st.session_state['chat_history'].add_message(HumanMessage(content=prompt))
   
    if account_number:
        user_data = query_user_data(account_number)
        if user_data:
            personalized_response = generate_personalized_response(user_data)
            
            # Append assistant message to chat history
            st.session_state['chat_history'].add_message(AIMessage(content=personalized_response))
            st.session_state['messages'].append({'role': 'assistant', 'content': personalized_response})
            return personalized_response
        else:
            st.error('No data found for the provided account number.')
            return None
    else:
        crawled_content = crawl_websites(urls)
        if not crawled_content:
            st.error('No content was retrieved from the URLs provided.')
            return None
        response = search_content(prompt, crawled_content)
        # Append assistant message to chat history
        st.session_state['chat_history'].add_message(AIMessage(content=response))
        return response

# Initialize session and settings
def setup_session_variables():
    st.session_state.setdefault("openai_model", "gpt-4o")
    st.session_state.setdefault("messages", [])

def display_messages():
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Main run function
def run_app():
    image = Image.open('logo.png')
    st.sidebar.image(image, width=70)

    st.sidebar.header("Configuration")
    st.sidebar.markdown('## Disclaimer')
    st.sidebar.markdown("This application is for demonstration purposes only. Please use it as a guide.")

    urls = toml.load(os.path.join(".streamlit", "secrets.toml"))['CRAWLER_URLS']

    setup_session_variables()
    display_messages()

    if prompt := st.chat_input("How may I assist you today?"):
        st.session_state["messages"].append({"role": "user", "content": prompt})
        response = process_prompt(prompt, urls)
        if response:
            st.session_state["messages"].append({"role": "assistant", "content": response})

if __name__ == "__main__":
    run_app()
