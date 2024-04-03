import os
import streamlit as st
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
import toml

secrets_path = os.path.join(".streamlit", "secrets.toml")
secrets = toml.load(secrets_path)

my_api_key = "sk-*****"
my_directory_path = "Set your data directory"

def setup_session_variables():
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4-turbo-preview"
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def process_prompt(prompt):
    Settings.llm = LlamaOpenAI(
        system_prompt = "Imagine you're a bank's wisest advisor, whose sole purpose is to navigate through the sea \
of financial queries regarding loans. Your guidance lights the way for those seeking to embark on the journey of securing \
a loan, unraveling the complexities of terms, conditions, and options available in the bank's treasure trove of data. \
Should a question arise that's beyond the mapped territories, gracefully suggest alternative routes of exploration, \
always ensuring your narrative enriches their understanding and decision-making process.",
        model = st.session_state["openai_model"],
        openai_api_key = my_api_key,
        max_tokens = 450
    )
    if os.path.isdir(my_directory_path):
        return search_directory(prompt)
    else:
        st.error(f"The path '{my_directory_path}' does not lead to a realm of knowledge. Please, correct it.")
        return None

def search_directory(prompt):
    documents = SimpleDirectoryReader(my_directory_path).load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine(streaming=True)
    streaming_response = query_engine.query(prompt)
    response_gen = streaming_response.response_gen
    return st.write_stream(response_gen)

def run_app():
    setup_session_variables()
    display_messages()

    if prompt := st.chat_input("How may I assist you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        response = process_prompt(prompt)
        if response:
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    run_app()
