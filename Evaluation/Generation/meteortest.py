import nltk
from nltk.translate.meteor_score import meteor_score
import pandas as pd
score_df = pd.read_csv('score_df.csv')
# Ensure you have the necessary NLTK resources
nltk.download('wordnet')

# Function to tokenize and compute METEOR score
def compute_meteor(reference, hypothesis):
    reference_tokens = reference.split()  # Tokenize the reference text
    hypothesis_tokens = hypothesis.split()  # Tokenize the hypothesis text
    return meteor_score([reference_tokens], hypothesis_tokens)

# Calculate METEOR scores for each query
score_df['meteor_score'] = score_df.apply(lambda row: compute_meteor(row['ground_truth'], row['answer']), axis=1)

# Print the DataFrame with METEOR scores
print(score_df[['question', 'meteor_score']])

# Calculate and print the average METEOR score across all queries
average_meteor = score_df['meteor_score'].mean()
print(f'Average METEOR Score: {average_meteor:.2f}')

# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib.pyplot import cm

# n = len(score_df)
# color = cm.rainbow(np.linspace(0, 1, n))

# plt.figure(figsize=(10, 6))
# plt.violinplot(score_df['meteor_score'], showmeans=True)
# plt.title('Distribution of METEOR Scores')
# plt.ylabel('METEOR Score')
# plt.show()


# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib.pyplot import cm

# n = len(score_df)
# color = cm.rainbow(np.linspace(0, 1, n))

# plt.figure(figsize=(10, 6))
# plt.boxplot(score_df['meteor_score'], patch_artist=True,
#             boxprops=dict(facecolor='lightblue', color='blue'),
#             medianprops=dict(color='blue'))
# for i, val in enumerate(score_df['meteor_score']):
#     plt.scatter(1, val, color=color[i], edgecolor='black', zorder=2)
# plt.title('Box Plot with Scatter Plot of METEOR Scores')
# plt.ylabel('METEOR Score')
# plt.show()






