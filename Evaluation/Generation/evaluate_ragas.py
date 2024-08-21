
import pandas as pd
from datasets import Dataset
from ragas.metrics import answer_correctness, context_precision, faithfulness, context_utilization
from ragas import evaluate
import ast
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from utils import load_secrets

def calculate_metrics(questions_csv: str, chunks_csv: str, output_csv: str) -> None:
    """
    Calculates evaluation metrics for the dataset and saves the results to a CSV file.

    Args:
        questions_csv (str): Path to the CSV file containing questions and generated answers.
        chunks_csv (str): Path to the CSV file containing chunks of context.
        output_csv (str): Path where the output CSV file with metrics will be saved.

    Returns:
        None
    """

    secrets = load_secrets()
    openai_api_key = secrets["OPENAI_API_KEY"]
    os.environ["OPENAI_API_KEY"] = openai_api_key

    questions_df = pd.read_csv(questions_csv)  
    chunks_df = pd.read_csv(chunks_csv)    

    questions_df['top_k_chunks'] = questions_df['top_k_chunks'].apply(ast.literal_eval)

    chunk_dict = pd.Series(chunks_df.chunk_content.values, index=chunks_df.chunk_number).to_dict()

    data_samples = {
        'question': [],
        'answer': [],
        'ground_truth': [],
        'contexts': []
    }

    for row in questions_df.iterrows():
        question = row['question']
        generated_answer = row['generated_answer'] 
        ground_truth = row['ground_truth']  
        top_k_chunks = row['top_k_chunks']

        contexts = [chunk_dict[chunk_id] for chunk_id in top_k_chunks if chunk_id in chunk_dict]
        
        data_samples['question'].append(question)
        data_samples['answer'].append(generated_answer)  
        data_samples['ground_truth'].append(ground_truth)  
        data_samples['contexts'].append(contexts)

    dataset = Dataset.from_dict(data_samples)

    score = evaluate(
        dataset,
        metrics=[answer_correctness, context_precision, faithfulness, context_utilization]
    )

    score_df = score.to_pandas()
    score_df.to_csv(output_csv, index=False)

    print(f"Metrics calculated and saved to {output_csv}")

if __name__ == "__main__":
    calculate_metrics('Evaluation/Generation/Files/QA_topk.csv', 'Evaluation/Generation/Files/chunks_content.csv', 'Evaluation/Generation/Files/Ragas_metrics.csv')