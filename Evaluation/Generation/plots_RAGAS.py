
import pandas as pd
import matplotlib.pyplot as plt

def generate_plots(score_csv: str) -> None:
    """
    Generates and displays plots for the metrics stored in the provided CSV file.

    Args:
        score_csv (str): Path to the CSV file containing the metrics.

    Returns:
        None
    """
    score_df = pd.read_csv(score_csv)

    plt.figure(figsize=(10, 6))
    plt.bar(range(len(score_df)), score_df['faithfulness'], color='blue')
    plt.title('Faithfulness Score Across Queries')
    plt.xlabel('Query Index')
    plt.ylabel('Faithfulness Score')
    plt.savefig('Evaluation/Generation/Plots/Faithfulness.png')

    plt.figure(figsize=(10, 6))
    plt.hist(score_df['answer_correctness'], bins=10, color='green', alpha=0.7)
    plt.title('Distribution of Answer Correctness Scores')
    plt.xlabel('Correctness Score')
    plt.ylabel('Frequency')
    plt.savefig('Evaluation/Generation/Plots/Frequency.png')

    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(score_df)), score_df['context_utilization'], color='red')
    plt.title('Context Utilization Across Queries')
    plt.xlabel('Query Index')
    plt.ylabel('Context Utilization Score')
    plt.savefig('Evaluation/Generation/Plots/Context Utilization.png')

    fig, ax1 = plt.subplots(figsize=(10, 6))
    color = 'tab:blue'
    ax1.set_xlabel('Query Index')
    ax1.set_ylabel('Context Precision', color=color)
    ax1.plot(range(len(score_df)), score_df['context_precision'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Context Utilization', color=color)
    ax2.plot(range(len(score_df)), score_df['context_utilization'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Context Precision vs. Context Utilization')
    plt.savefig('Evaluation/Generation/Plots/Precision_Utilization.png')
    plt.close()

if __name__ == "__main__":
    generate_plots('Evaluation/Generation/Files/generation_metrics.csv')