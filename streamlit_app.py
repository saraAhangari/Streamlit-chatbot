import os
import streamlit as st
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader

def setup_session_variables():
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4-turbo-preview"
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def process_prompt(prompt, my_directory_path):
    Settings.llm = LlamaOpenAI(
    system_prompt = "As the most knowledgeable advisor within the digital realm, this LLM model is designed to navigate \
    the vast ocean of information contained in a specific directory provided by the user. With the key to access (user's own API key), \
    it dives deep into the specified data, ready to surface with insights and answers. It's your go-to source for unravelling \
    the intricacies found within your chosen path of data. In cases where inquiries stray beyond the bounds of the directory's knowledge, \
    the model will humbly apologize, indicating its expertise is confined to the realms of the specified information. It's here to \
    enrich your understanding and guide your decision-making process within the context of your specified data.",
    model = st.session_state["openai_model"],
    openai_api_key = "ENTER_YOUR_API_KEY_HERE",
    max_tokens = 450
)

    if os.path.isdir(my_directory_path):
        return search_directory(prompt, my_directory_path)
    else:
        st.error(f"The path '{my_directory_path}' does not lead to a realm of knowledge. Please, correct it.")
        return None

def search_directory(prompt, my_directory_path):
    documents = SimpleDirectoryReader(my_directory_path).load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine(streaming=True)
    streaming_response = query_engine.query(prompt)
    response_gen = streaming_response.response_gen
    return st.write_stream(response_gen)

def run_app():
    st.sidebar.header("Configuration")
    my_api_key = st.sidebar.text_input("Your OpenAI API key:", type="password")
    my_directory_path = st.sidebar.text_input("Your data directory path:")

    setup_session_variables()
    display_messages()

    if prompt := st.chat_input("How may I assist you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        response = process_prompt(prompt, my_api_key, my_directory_path)
        if response:
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    run_app()
