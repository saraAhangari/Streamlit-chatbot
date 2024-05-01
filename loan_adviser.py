import os
import streamlit as st
import pandas as pd
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
import toml
from PIL import Image
from streamlit_pills import pills
from sqlalchemy import create_engine, inspect, text
from llama_index.core.query_engine import NLSQLTableQueryEngine
import psycopg2

secrets_path = os.path.join(".streamlit", "secrets.toml")
secrets = toml.load(secrets_path)

my_api_key = secrets['OPENAI_API_KEY']
my_directory_path = secrets['DATA_DIRECTORY_PATH']

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

def get_table_data(table_name, conn):
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, conn)
            return df    

# def load_db_llm():
#     engine = create_engine()
#     sql_database = SQLDatabase(engine)
#     return sql_database, engine            

def run_app():
    image = Image.open('logo.png')
    st.sidebar.image(image, width=70)
    # sql_database, engine = load_db_llm()
    setup_session_variables()
    display_messages()

    st.sidebar.markdown("## Database Schema Viewer")
    # inspector = inspect(engine)
    # table_names = inspector.get_table_names()
    # selected_table = st.sidebar.selectbox("Select a Table", table_names)
    # db_file = ''
    # conn = psycopg2.connect(db_file)
    # if selected_table:
    #     df = get_table_data(selected_table, conn)
    #     st.sidebar.text(f"Data for table '{selected_table}':")
    #     st.sidebar.dataframe(df)

    # conn.close()    

    # if "query_engine" not in st.session_state:  # Initialize the query engine
    #     st.session_state["query_engine"] = NLSQLTableQueryEngine(
    #         # sql_database=sql_database,
    #         synthesize_response=True,
    #     )

    if prompt := st.chat_input("How may I assist you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        query_options = ["In a markdown table format show which me all the loans available in this bank"]
        selected_query = pills("Select example queries or enter your own query in the chat input below", query_options, key="query_pills")
        with st.chat_message("user"):
            st.markdown(prompt)
        response = process_prompt(prompt)
        if response:
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    run_app()
