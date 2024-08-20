import logging

import requests
import streamlit as st
from bs4 import BeautifulSoup


def crawl_webpage(url: str) -> str:
    """
    Crawl a single webpage and return the text content.

    Args:
        url (str): URL of the webpage to crawl.

    Returns:
        str: Text content of the crawled webpage.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text(separator=' ')
    except requests.RequestException as e:
        logging.error(f"Error crawling {url}: {e}")
        st.error(f"Error crawling {url}: {e}")
        return ""

def crawl_websites(urls: list) -> str:
    """
    Crawl multiple websites and concatenate their text content.

    Args:
        urls (list): List of URLs to crawl.

    Returns:
        str: Concatenated text content from all crawled websites.
    """
    return "".join(crawl_webpage(url) for url in urls)
