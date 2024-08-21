import pandas as pd
from bert_score import score


def compute_bert_score(input_csv: str, output_csv: str) -> pd.DataFrame:
    """
    Computes the BERTScore F1 for each pair of ground truth and generated answers in the input CSV.
    The results are saved to the output CSV file, and the average BERTScore is printed.

    Args:
        input_csv (str): Path to the input CSV file containing the data.
        output_csv (str): Path to the output CSV file where the results with BERTScore will be saved.

    Returns:
        pd.DataFrame: DataFrame containing the data along with the computed BERTScore F1.
    """
    score_df = pd.read_csv(input_csv)
    references = score_df['ground_truth'].tolist()
    candidates = score_df['answer'].tolist()

    P, R, F1 = score(candidates, references, lang="en", verbose=True)

    score_df['BERTScore'] = F1.numpy()
    score_df = score_df[['question', 'answer_correctness', 'context_precision', 'faithfulness', 'context_utilization', 'BERTScore']]
    score_df.to_csv(output_csv, index=False)

    average_bert_score = score_df['BERTScore'].mean()
    print(f'Average BERTScore F1: {average_bert_score:.2f}')

    return score_df

if __name__ == "__main__":
    input_csv_path = 'Evaluation/Generation/Files/all_scores.csv'
    output_csv_path = 'Evaluation/Generation/Files/generation_metrics.csv'
    compute_bert_score(input_csv_path, output_csv_path)
