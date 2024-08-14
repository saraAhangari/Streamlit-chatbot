import os

import streamlit as st
import toml

SECRETS_PATH = os.path.join("./.streamlit", "secrets.toml")

def load_secrets() -> dict:
    return toml.load(SECRETS_PATH)

def setup_session_variables() -> None:
    """
    Initialize session variables if they are not already set.
    """
    st.session_state.setdefault("openai_model", "gpt-4o")
    st.session_state.setdefault("messages", [])

def display_messages() -> None:
    """
    Display chat messages stored in the session state.
    """
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
