import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.pyplot import cm


def generate_plots(score_csv: str) -> None:
    """
    Generates and displays plots for the metrics stored in the provided CSV file.

    Args:
        score_csv (str): Path to the CSV file containing the metrics.

    Returns:
        None
    """
    score_df = pd.read_csv(score_csv)

    n = len(score_df)
    color = cm.rainbow(np.linspace(0, 1, n))

    plt.figure(figsize=(10, 6))
    plt.violinplot(score_df['meteor_score'], showmeans=True)
    plt.title('Distribution of METEOR Scores')
    plt.ylabel('METEOR Score')
    plt.savefig('Evaluation/Generation/Plots/METEOR Score Distribution.png')


    plt.figure(figsize=(10, 6))
    plt.boxplot(score_df['meteor_score'], patch_artist=True,
                boxprops=dict(facecolor='lightblue', color='blue'),
                medianprops=dict(color='blue'))
    for i, val in enumerate(score_df['meteor_score']):
        plt.scatter(1, val, color=color[i], edgecolor='black', zorder=2)
    plt.title('Box Plot with Scatter Plot of METEOR Scores')
    plt.ylabel('METEOR Score')
    plt.savefig('Evaluation/Generation/Plots/METEOR Score Box Plot.png')

if __name__ == "__main__":
    generate_plots('Evaluation/Generation/Files/generation_metrics.csv')