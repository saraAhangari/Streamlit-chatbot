import os
import streamlit as st
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from PIL import Image
import toml
from llama_index.embeddings.openai import OpenAIEmbedding

secrets_path = os.path.join(".streamlit", "secrets.toml")
secrets = toml.load(secrets_path)

api_key = secrets['OPENAI_API_KEY']
directory_path = secrets['DATA_DIRECTORY_PATH']

def setup_session_variables():
    st.session_state.setdefault("openai_model", "gpt-4-turbo-preview")
    st.session_state.setdefault("messages", [])

def display_messages():
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def process_prompt(prompt, api_key, directory_path):
    system_prompt = """Imagine you're a wisest advisor for Blu bank, whose sole purpose is to navigate through the sea \
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
    if not os.path.isdir(directory_path):
        st.error(f"The path '{directory_path}' does not lead to a realm of knowledge. Please correct it.")
        return None
    return search_directory(prompt, directory_path)

def search_directory(prompt, directory_path):
    documents = SimpleDirectoryReader(directory_path).load_data()
    index = VectorStoreIndex.from_documents(documents)
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

    directory_path = toml.load(os.path.join(".streamlit", "secrets.toml"))['DATA_DIRECTORY_PATH']

    setup_session_variables()
    display_messages()

    if prompt := st.chat_input("How may I assist you today?"):
        st.session_state["messages"].append({"role": "user", "content": prompt})
        response = process_prompt(prompt, api_key, directory_path)
        if response:
            st.session_state["messages"].append({"role": "assistant", "content": response})

if __name__ == "__main__":
    run_app()
