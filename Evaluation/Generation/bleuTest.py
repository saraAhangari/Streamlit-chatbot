import pandas as pd
import ast
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# Assuming you have a DataFrame `score_df` with generated answers and ground truth
# Example columns in score_df: ['question', 'generated_answer', 'ground_truth']
score_df = pd.read_csv('Evaluation/Generation/score_df.csv')

# Function to compute BLEU score for a single pair of generated and ground truth answers
def compute_bleu(reference, hypothesis):
    reference = [reference.split()]  # BLEU expects a list of references, each being a list of tokens
    hypothesis = hypothesis.split()   # Hypothesis is a list of tokens
    smoothie = SmoothingFunction().method4  # Optional: Smooth out zero counts in BLEU score calculation
    return sentence_bleu(reference, hypothesis, smoothing_function=smoothie)

# Calculate BLEU scores for each query
score_df['bleu_score'] = score_df.apply(lambda row: compute_bleu(row['ground_truth'], row['answer']), axis=1)

# Print the DataFrame with BLEU scores
print(score_df[['question', 'bleu_score']])

# Calculate and print the average BLEU score across all queries
average_bleu = score_df['bleu_score'].mean()
print(f'Average BLEU Score: {average_bleu:.2f}')


import matplotlib.pyplot as plt

# Assuming score_df already has the 'bleu_score' column from the previous step

# Bar Plot of BLEU Scores for Each Query
plt.figure(figsize=(12, 6))
plt.bar(range(len(score_df)), score_df['bleu_score'], color='blue', alpha=0.7)
plt.title('BLEU Scores Across Queries')
plt.xlabel('Query Index')
plt.ylabel('BLEU Score')
plt.xticks(ticks=range(len(score_df)), labels=score_df['question'], rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Histogram of BLEU Score Distribution
plt.figure(figsize=(10, 6))
plt.hist(score_df['bleu_score'], bins=10, color='green', alpha=0.7)
plt.title('Distribution of BLEU Scores')
plt.xlabel('BLEU Score')
plt.ylabel('Frequency')
plt.show()

