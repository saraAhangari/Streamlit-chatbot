import os
import csv
from utils import split_text, load_secrets
from database import get_postgres_connection
from web_crawler import crawl_websites

def extract_chunks_to_csv(text: str, csv_path: str, chunk_size: int = 500, overlap: int = 50) -> None:
    """
    Extract chunks from the provided text and save them to a CSV file.

    Args:
        text (str): The text to split into chunks.
        csv_path (str): The path where the CSV file will be saved.
        chunk_size (int, optional): The size of each chunk. Defaults to 500.
        overlap (int, optional): The overlap between chunks. Defaults to 50.

    Returns:
        None
    """
    chunks = split_text(text, chunk_size=chunk_size, overlap=overlap)

    # Write chunks to CSV
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["chunk_number", "chunk_content"])  # Write headers
        for i, chunk in enumerate(chunks):
            writer.writerow([i + 1, chunk])  # Write chunk number and content

    print(f"Chunks have been saved to {csv_path}")

def crawl_and_save_chunks_to_csv(urls: list, csv_path: str) -> None:
    """
    Crawl websites, extract chunks, and save them to a CSV file.

    Args:
        urls (list): List of URLs to crawl for generating text chunks.
        csv_path (str): The path where the CSV file will be saved.

    Returns:
        None
    """
    # Crawl the websites and retrieve content
    web_content = crawl_websites(urls)
    
    # Extract and save chunks to CSV
    extract_chunks_to_csv(web_content, csv_path)

if __name__ == "__main__":
    secrets = load_secrets()
    urls = secrets['CRAWLER_URLS']
    
    # Define the path to save the CSV file in the Downloads folder
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    csv_path = os.path.join(downloads_folder, 'chunks.csv')
    
    # Crawl and save chunks to CSV
    crawl_and_save_chunks_to_csv(urls, csv_path)
