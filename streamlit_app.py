import os
import streamlit as st
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.core import Settings, VectorStoreIndex, Document
from PIL import Image
import toml
from llama_index.embeddings.openai import OpenAIEmbedding
import requests
from bs4 import BeautifulSoup

secrets_path = os.path.join(".streamlit", "secrets.toml")
secrets = toml.load(secrets_path)

api_key = secrets['OPENAI_API_KEY']
urls = secrets['CRAWLER_URLS'] 

def setup_session_variables():
    st.session_state.setdefault("openai_model", "gpt-4-turbo-preview")
    st.session_state.setdefault("messages", [])

def display_messages():
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def crawl_webpage(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text(separator=' ')
    except Exception as e:
        st.error(f"Error crawling {url}: {str(e)}")
        return ""

def crawl_websites(urls):
    content = ""
    for url in urls:
        content += crawl_webpage(url)
    return content

def process_prompt(prompt, api_key, urls):
    system_prompt = """Imagine you're the wisest advisor for Blu bank, whose sole purpose is to navigate through the sea \
    of financial queries regarding loans. Your guidance lights the way for those seeking to embark on the journey of securing \
    a loan, unraveling the complexities of terms, conditions, and options available in the bank's treasure trove of data. \
    Should a question arise that's beyond the mapped territories, gracefully suggest alternative routes of exploration, \
    always ensuring your narrative enriches their understanding and decision-making process."""
    
    Settings.llm = LlamaOpenAI(
        model=st.session_state["openai_model"],
        openai_api_key=api_key,
        max_tokens=450,
        system_prompt=system_prompt
    )
    Settings.embed_model = OpenAIEmbedding()

    crawled_content = crawl_websites(urls)
    
    if not crawled_content:
        st.error("No content was retrieved from the URLs provided.")
        return None

    return search_content(prompt, crawled_content)

def search_content(prompt, content):
    document = Document(text=content)
    
    index = VectorStoreIndex.from_documents([document])
    query_engine = index.as_query_engine(streaming=True)
    streaming_response = query_engine.query(prompt)
    response_gen = streaming_response.response_gen
    return st.write_stream(response_gen)

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
        response = process_prompt(prompt, api_key, urls)
        if response:
            st.session_state["messages"].append({"role": "assistant", "content": response})

if __name__ == "__main__":
    run_app()