import ast
import os
import sys

import nltk
import pandas as pd
from bert_score import score
from datasets import Dataset
from nltk.translate.meteor_score import meteor_score
from ragas import evaluate
from ragas.metrics import (answer_correctness, context_precision,
                           context_utilization, faithfulness)

nltk.download('wordnet')

sys.path.insert(1, '/home/baranahangari/Desktop/Streamlit-chatbot/src')

from utils import load_secrets


def calculate_ragas_metrics(questions_csv: str, chunks_csv: str) -> pd.DataFrame:
    """
    Calculates RAGAS evaluation metrics and returns the results as a DataFrame.

    Args:
        questions_csv (str): Path to the CSV file containing questions and generated answers.
        chunks_csv (str): Path to the CSV file containing chunks of context.

    Returns:
        pd.DataFrame: DataFrame containing RAGAS metrics.
    """

    secrets = load_secrets()
    openai_api_key = secrets["OPENAI_API_KEY"]
    os.environ["OPENAI_API_KEY"] = openai_api_key

    questions_df = pd.read_csv(questions_csv)  # contains question, top_k_chunks, generated_answer
    chunks_df = pd.read_csv(chunks_csv)    # contains chunk_number and chunk_content

    # Convert the 'top_k_chunks' from string representation of lists to actual lists
    questions_df['top_k_chunks'] = questions_df['top_k_chunks'].apply(ast.literal_eval)

    # Create a dictionary to map chunk_number to chunk_content
    chunk_dict = pd.Series(chunks_df.chunk_content.values, index=chunks_df.chunk_number).to_dict()

    # Prepare the data samples for RAGAS
    data_samples = {
        'question': [],
        'answer': [],
        'ground_truth': [],
        'contexts': []
    }

    # Fill in the data_samples by mapping top_k_chunks to their corresponding chunk_content
    for index, row in questions_df.iterrows():
        question = row['question']
        generated_answer = row['generated_answer']  # Get the generated answer
        ground_truth = row['ground_truth']  # Get the ground truth
        top_k_chunks = row['top_k_chunks']

        # Retrieve the corresponding chunk contents
        contexts = [chunk_dict[chunk_id] for chunk_id in top_k_chunks if chunk_id in chunk_dict]
        
        # Append to data_samples
        data_samples['question'].append(question)
        data_samples['answer'].append(generated_answer)  # Use the actual generated answer
        data_samples['ground_truth'].append(ground_truth)  # Use the actual ground truth answer
        data_samples['contexts'].append(contexts)

    # Create the Dataset object
    dataset = Dataset.from_dict(data_samples)

    # Evaluate the dataset with selected metrics
    score = evaluate(
        dataset,
        metrics=[answer_correctness, context_precision, faithfulness, context_utilization]
    )

    # Convert the score to a pandas DataFrame for easier analysis
    score_df = score.to_pandas()
    return score_df

def calculate_meteor_scores(score_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates METEOR scores for each query in the input CSV and saves the results to a new CSV file.

    Args:
        input_csv (str): Path to the input CSV file containing the data.
        output_csv (str): Path to the output CSV file where the results with METEOR scores will be saved.

    Returns:
        pd.DataFrame: DataFrame containing the data along with calculated METEOR scores.
    """

    # Function to tokenize and compute METEOR score
    def compute_meteor(reference: str, hypothesis: str) -> float:
        reference_tokens = reference.split()  # Tokenize the reference text
        hypothesis_tokens = hypothesis.split()  # Tokenize the hypothesis text
        return meteor_score([reference_tokens], hypothesis_tokens)
    
    new_df = pd.DataFrame()

    # Calculate METEOR scores for each query
    new_df['meteor_score'] = score_df.apply(lambda row: compute_meteor(row['ground_truth'], row['generated_answer']), axis=1)

    # Calculate and print the average METEOR score across all queries
    average_meteor = new_df['meteor_score'].mean()
    print(f'Average METEOR Score: {average_meteor:.2f}')

    return new_df

def calculate_bert_score(references: list, predictions: list) -> pd.DataFrame:
    """
    Calculates BERTScore for the given references and predictions.

    Args:
        references (list): List of reference texts.
        predictions (list): List of predicted texts.

    Returns:
        pd.DataFrame: DataFrame containing BERTScores.
    """
    bert_df = pd.DataFrame()
    P, R, F1 = score(references, predictions, lang="en", verbose=True)
    bert_df['BERTScore'] = F1.numpy()

    average_bert_score = bert_df['BERTScore'].mean()
    print(f'Average BERTScore F1: {average_bert_score:.2f}')

    return bert_df

def calculate_all_metrics(questions_csv: str, chunks_csv: str, output_csv: str) -> None:
    """
    Calculates RAGAS, METEOR, and BERTScore metrics and saves the combined results to a CSV file.

    Args:
        questions_csv (str): Path to the CSV file containing questions and generated answers.
        chunks_csv (str): Path to the CSV file containing chunks of context.
        output_csv (str): Path where the output CSV file with all metrics will be saved.

    Returns:
        None
    """
    # Calculate RAGAS metrics
    ragas_df = calculate_ragas_metrics(questions_csv, chunks_csv)

    # Load questions and answers
    questions_df = pd.read_csv(questions_csv)
    references = questions_df['ground_truth'].tolist()
    predictions = questions_df['generated_answer'].tolist()

    # Calculate BERTScore
    bert_df = calculate_bert_score(references, predictions)

    # Calculate METEOR scores
    meteor_df = calculate_meteor_scores(questions_df, )


    # Combine all metrics into one DataFrame
    combined_df = pd.concat([ragas_df, meteor_df, bert_df], axis=1)
    combined_df = combined_df[['question', 'answer_correctness', 'context_precision', 'faithfulness', 'context_utilization','bert_score', 'meteor_score']]

    combined_df.to_csv(output_csv, index=False)

    print(f"All metrics calculated and saved to {output_csv}")

if __name__ == "__main__":
    calculate_all_metrics('Evaluation/Generation/Files/QA_topk.csv', 'Evaluation/Generation/Files/chunks_content.csv', 'Evaluation/Generation/Files/all_metrics.csv')
