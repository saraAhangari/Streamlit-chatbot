import streamlit as st
from PIL import Image

from chat import process_prompt
from database import get_postgres_connection
from utils import load_secrets, setup_session_variables

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

def run_app() -> None:
    """Runs the Streamlit app for the chat interface."""
    image = Image.open('logo.png')
    st.sidebar.image(image, width=70)

    st.sidebar.header("Configuration")
    st.sidebar.markdown('## Disclaimer')
    st.sidebar.markdown("This application is for demonstration purposes only. Please use it as a guide.")

    secrets = load_secrets()
    urls = secrets['CRAWLER_URLS']
    engine = get_postgres_connection(secrets['postgres'])

    if not engine:
        st.error("Failed to connect to the database.")
        return
    
    setup_session_variables()

    for chat in st.session_state.chat_history:
        st.chat_message(chat["role"]).markdown(chat["content"])

    prompt = st.chat_input("Ask me anything...")

    if prompt:
        response = process_prompt(prompt, urls, engine)
        st.chat_message("user").markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.session_state.chat_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    run_app()
