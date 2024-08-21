from bert_score import score
import pandas as pd

score_df = pd.read_csv('score_df.csv')
# Assuming your data is in score_df
# Example: Compute BERTScore
references = score_df['ground_truth'].tolist()
candidates = score_df['answer'].tolist()

P, R, F1 = score(candidates, references, lang="en", verbose=True)

# Add the F1 BERTScore to the DataFrame
score_df['bert_score'] = F1.numpy()
score_df.to_csv('bert_score.csv', index=False)
# Print the average BERTScore
average_bert_score = score_df['bert_score'].mean()
print(f'Average BERTScore F1: {average_bert_score:.2f}')
