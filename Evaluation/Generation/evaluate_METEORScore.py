import nltk
import pandas as pd
from nltk.translate.meteor_score import meteor_score


def compute_meteor_scores(input_csv: str, output_csv: str) -> pd.DataFrame:
    """
    Computes METEOR scores for each query in the input CSV file and saves the results to a new CSV file.

    Args:
        input_csv (str): Path to the input CSV file containing the data.
        output_csv (str): Path to the output CSV file where the results with METEOR scores will be saved.

    Returns:
        pd.DataFrame: DataFrame containing the data along with the computed METEOR scores.
    """
    nltk.download('wordnet')
    score_df = pd.read_csv(input_csv)

    def compute_meteor(reference: str, hypothesis: str) -> float:
        reference_tokens = reference.split()
        hypothesis_tokens = hypothesis.split()
        return meteor_score([reference_tokens], hypothesis_tokens)

    score_df['meteor_score'] = score_df.apply(lambda row: compute_meteor(row['ground_truth'], row['answer']), axis=1)
    score_df = score_df[['question', 'answer_correctness', 'context_precision', 'faithfulness', 'context_utilization', 'bert_score', 'meteor_score']]
    score_df.to_csv(output_csv, index=False)

    average_meteor = score_df['meteor_score'].mean()
    print(f'Average METEOR Score: {average_meteor:.2f}')

    return score_df

if __name__ == "__main__":
    input_csv_path = 'Evaluation/Generation/Files/all_scores.csv'
    output_csv_path = 'Evaluation/Generation/Files/generation_metrics.csv'
    compute_meteor_scores(input_csv_path, output_csv_path)
