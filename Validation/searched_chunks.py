import os
import sys

import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from utils import load_secrets
from web_crawler import crawl_websites


def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """
    Split text into chunks of a specified size with an overlap.

    Args:
        text (str): The text to split.
        chunk_size (int, optional): The size of each chunk. Defaults to 500.
        overlap (int, optional): The overlap between chunks. Defaults to 50.

    Returns:
        list: List of text chunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def get_chunks(questions: list, urls: list) -> pd.DataFrame:
    """
    Process a list of questions, retrieve the selected chunks for each, and return a DataFrame.

    Args:
        questions (list): List of questions to process.
        urls (list): List of URLs to crawl for generating text chunks.

    Returns:
        pd.DataFrame: DataFrame containing the question, expected chunks (empty), and selected chunks.
    """
    
    web_content = crawl_websites(urls)
    
    chunks = split_text(web_content)
    
    df = pd.DataFrame(columns=["question", "expected_chunks", "selected_chunks"])
    
    for question in questions:
        selected_chunks = select_chunks_for_question(question, chunks) 
        
        new_row = pd.DataFrame([{
            "question": question,
            "expected_chunks": "",  
            "selected_chunks": selected_chunks
        }])
        
        df = pd.concat([df, new_row], ignore_index=True)
    
    return df

def select_chunks_for_question(question: str, chunks: list) -> list:
    """
    Select chunks based on keyword matching.

    Args:
        question (str): The user's input question.
        chunks (list): List of text chunks.

    Returns:
        list: List of indices of the selected chunks.
    """
    selected_indices = []
    
    for i, chunk in enumerate(chunks):
        if any(word in chunk for word in question.split()):
            selected_indices.append(i)
    
    return selected_indices

if __name__ == "__main__":
    secrets = load_secrets()
    urls = secrets['CRAWLER_URLS']
    
    questions = [
        "چگونه می‌توان از بلوبانک وام دریافت کرد؟",
        "حداقل میانگین حساب برای دریافت وام از بلوبانک چقدر است؟",
        "سقف وام‌های بلوبانک چقدر است؟",
        "مدت زمان بازپرداخت وام‌های بلوبانک چقدر است؟",
        "آیا برای دریافت وام از بلوبانک نیاز به ضامن است؟",
        "چه نوع وثیقه‌ای برای دریافت وام از بلوبانک نیاز است؟",
        "چگونه می‌توان اعتبارسنجی خود را در بلوبانک بهبود داد؟",
        "آیا امکان دریافت وام بدون داشتن حساب فعال در بلوبانک وجود دارد؟",
        "فرآیند درخواست وام از بلوبانک چگونه است؟",
        "چگونه می‌توان وضعیت درخواست وام را در بلوبانک پیگیری کرد؟",
        "آیا بلوبانک نرخ بهره مشخصی برای وام‌ها دارد؟",
        "آیا امکان تغییر شرایط بازپرداخت وام در بلوبانک وجود دارد؟",
        "آیا بلوبانک وام‌های بلندمدت ارائه می‌دهد؟",
        "چه مدارکی برای درخواست وام در بلوبانک نیاز است؟",
        "چگونه می‌توان از پیشنهادات ویژه وام‌های بلوبانک مطلع شد؟",
        "آیا امکان دریافت وام دوم از بلوبانک پس از بازپرداخت وام اول وجود دارد؟",
        "آیا بلوبانک برای دانشجویان نیز وام ارائه می‌دهد؟",
        "چه عواملی می‌توانند باعث رد شدن درخواست وام در بلوبانک شوند؟",
        "آیا بلوبانک طرح‌های تشویقی برای مشتریان وام‌گیرنده دارد؟",
        "چگونه می‌توان از خدمات پشتیبانی بلوبانک در مورد وام‌ها استفاده کرد؟"
    ]
    
    df = get_chunks(questions, urls)
    df.to_csv('Validation/Files/all_searched_chunks.csv', index=False)