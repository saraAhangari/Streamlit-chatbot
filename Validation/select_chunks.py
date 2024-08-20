import sys
import pandas as pd
import os


# Add the src directory to the path to allow imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from utils import split_text, load_secrets
from web_crawler import crawl_websites

def process_questions_and_get_chunks(questions: list, urls: list) -> pd.DataFrame:
    """
    Process a list of questions, retrieve the selected chunks for each, and return a DataFrame.

    Args:
        questions (list): List of questions to process.
        urls (list): List of URLs to crawl for generating text chunks.

    Returns:
        pd.DataFrame: DataFrame containing the question, expected chunks (empty), and selected chunks.
    """
    # Crawl the websites and retrieve content
    web_content = crawl_websites(urls)
    
    # Split the content into chunks
    chunks = split_text(web_content)
    
    # Initialize the DataFrame
    df = pd.DataFrame(columns=["question", "expected_chunks", "selected_chunks"])
    
    for question in questions:
        selected_chunks = select_chunks_for_question(question, chunks)  # Replace this with actual model logic
        
        # Create a new row as a DataFrame
        new_row = pd.DataFrame([{
            "question": question,
            "expected_chunks": "",  # To be filled manually later
            "selected_chunks": selected_chunks
        }])
        
        # Use concat to add the new row to the DataFrame
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
    
    # Basic keyword matching to select relevant chunks
    for i, chunk in enumerate(chunks):
        # Check if any word from the question is in the chunk
        if any(word in chunk for word in question.split()):
            selected_indices.append(i)
    
    return selected_indices

if __name__ == "__main__":
    secrets = load_secrets()
    urls = secrets['CRAWLER_URLS']
    
    # List of questions in Persian
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
    
    # Process questions and generate the DataFrame
    df = process_questions_and_get_chunks(questions, urls)
    df.to_csv('answer.csv', index=False)
    
    # Output the DataFrame
    print(df)
