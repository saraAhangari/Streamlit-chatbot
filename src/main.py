import streamlit as st
from langchain_community.chat_message_histories.in_memory import \
    ChatMessageHistory
from PIL import Image

from chat import process_prompt
from database import get_postgres_connection
from utils import display_messages, load_secrets, setup_session_variables

# Initialize ChatMessageHistory
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = ChatMessageHistory()

def run_app() -> None:
    """
    Main function to run the Streamlit app.
    """
    image = Image.open('logo.png')
    st.sidebar.image(image, width=70)

    st.sidebar.header("Configuration")
    st.sidebar.markdown('## Disclaimer')
    st.sidebar.markdown("This application is for demonstration purposes only. Please use it as a guide.")

    secrets = load_secrets()
    urls = secrets['CRAWLER_URLS']
    engine = get_postgres_connection(secrets['postgres'])

    setup_session_variables()
    display_messages()

    if prompt := st.chat_input("How may I assist you today?"):
        st.session_state["messages"].append({"role": "user", "content": prompt})
        response = process_prompt(prompt, urls, engine)
        if response:
            st.session_state["messages"].append({"role": "assistant", "content": response})

if __name__ == "__main__":
    run_app()
