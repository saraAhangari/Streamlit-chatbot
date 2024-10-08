import csv
import os

from utils import load_secrets, split_text
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

    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["chunk_number", "chunk_content"])  
        for i, chunk in enumerate(chunks):
            writer.writerow([i + 1, chunk])  

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

    web_content = crawl_websites(urls)
    
    extract_chunks_to_csv(web_content, csv_path)

if __name__ == "__main__":
    secrets = load_secrets()
    urls = secrets['CRAWLER_URLS']
    
    path_folder = os.path.join(os.path.expanduser('~'), 'Evaluation/Retrieve/Files')
    csv_path = os.path.join(path_folder, 'chunks_content.csv')
    
    crawl_and_save_chunks_to_csv(urls, csv_path)
