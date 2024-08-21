import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.pyplot import cm
from pandas.plotting import parallel_coordinates


def create_violin_plot(df: pd.DataFrame) -> None:
    """
    Creates and saves a violin plot showing the distribution of overlap accuracy, proximity accuracy,
    and partial match accuracy.

    Parameters:
        df (pd.DataFrame): DataFrame containing the accuracy metrics.
    """
    plt.figure(figsize=(12, 6))
    plt.violinplot([df['overlap_accuracy'], df['proximity_accuracy'], df['partial_match_accuracy']])
    plt.xticks([1, 2, 3], ['Overlap Accuracy', 'Proximity Accuracy', 'Partial Match Accuracy'])
    plt.title('Distribution of Accuracy Metrics')
    plt.xlabel('Metric')
    plt.ylabel('Accuracy')
    plt.savefig('Evaluation/Retrieve/Plots/violin_plot.png')
    plt.close()

def create_box_swarm_plot(df: pd.DataFrame) -> None:
    """
    Creates and saves a box plot with scatter plot (simulated swarm plot) for the accuracy metrics.

    Parameters:
        df (pd.DataFrame): DataFrame containing the accuracy metrics.
    """
    plt.figure(figsize=(12, 6))
    plt.boxplot([df['overlap_accuracy'], df['proximity_accuracy'], df['partial_match_accuracy']], patch_artist=True,
                boxprops=dict(facecolor='lightblue', color='blue'),
                medianprops=dict(color='blue'))

    colors = cm.rainbow(np.linspace(0, 1, len(df)))
    for i, metric in enumerate(['overlap_accuracy', 'proximity_accuracy', 'partial_match_accuracy']):
        plt.scatter([i+1]*len(df), df[metric], color=colors, edgecolor='black', alpha=0.6)

    plt.xticks([1, 2, 3], ['Overlap Accuracy', 'Proximity Accuracy', 'Partial Match Accuracy'])
    plt.title('Box Plot with Scatter Plot of Accuracy Metrics')
    plt.xlabel('Metric')
    plt.ylabel('Accuracy')
    plt.savefig('Evaluation/Retrieve/Plots/box_swarm_plot.png')
    plt.close()

def create_radar_chart(df: pd.DataFrame) -> None:
    """
    Creates and saves a radar chart showing the mean values of overlap accuracy, proximity accuracy,
    and partial match accuracy.

    Parameters:
        df (pd.DataFrame): DataFrame containing the accuracy metrics.
    """
    metrics_df = df[['overlap_accuracy', 'proximity_accuracy', 'partial_match_accuracy']]
    mean_values = metrics_df.mean().values
    mean_values = np.append(mean_values, mean_values[0])
    metrics = ['Overlap Accuracy', 'Proximity Accuracy', 'Partial Match Accuracy']
    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, mean_values, color=cm.rainbow(0), alpha=0.25)
    ax.plot(angles, mean_values, color=cm.rainbow(0), linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics)
    plt.title('Radar Chart of Accuracy Metrics')
    plt.savefig('Evaluation/Retrieve/Plots/radar_chart.png')
    plt.close()

def create_heatmap(df: pd.DataFrame) -> None:
    """
    Creates and saves a heatmap showing the correlation between the accuracy metrics.

    Parameters:
        df (pd.DataFrame): DataFrame containing the accuracy metrics.
    """
    corr_matrix = df[['overlap_accuracy', 'proximity_accuracy', 'partial_match_accuracy']].corr()
    plt.figure(figsize=(8, 6))
    plt.imshow(corr_matrix, cmap="coolwarm", interpolation='nearest')
    plt.colorbar(label='Correlation Coefficient')

    for i in range(len(corr_matrix)):
        for j in range(len(corr_matrix)):
            plt.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}', ha='center', va='center', color='black')

    plt.xticks(ticks=np.arange(len(corr_matrix.columns)), labels=corr_matrix.columns, rotation=45, ha="right")
    plt.yticks(ticks=np.arange(len(corr_matrix.index)), labels=corr_matrix.index)
    plt.title('Correlation Heatmap of Accuracy Metrics')
    plt.tight_layout()
    plt.savefig('Evaluation/Retrieve/Plots/heatmap.png')
    plt.close()

def create_joint_plot(df: pd.DataFrame) -> None:
    """
    Creates and saves a joint plot (scatter plot with regression line) of overlap accuracy vs proximity accuracy.

    Parameters:
        df (pd.DataFrame): DataFrame containing the accuracy metrics.
    """
    plt.figure(figsize=(8, 8))
    plt.scatter(df['overlap_accuracy'], df['proximity_accuracy'], color=cm.rainbow(0.5), alpha=0.6)
    plt.title('Joint Plot of Overlap Accuracy vs Proximity Accuracy')
    plt.xlabel('Overlap Accuracy')
    plt.ylabel('Proximity Accuracy')

    m, b = np.polyfit(df['overlap_accuracy'], df['proximity_accuracy'], 1)
    plt.plot(df['overlap_accuracy'], m*df['overlap_accuracy'] + b, color='black', linewidth=2)

    plt.savefig('Evaluation/Retrieve/Plots/joint_plot.png')
    plt.close()

def create_parallel_coordinates_plot(df: pd.DataFrame) -> None:
    """
    Creates and saves a parallel coordinates plot for the accuracy metrics.

    Parameters:
        df (pd.DataFrame): DataFrame containing the accuracy metrics.
    """
    plt.figure(figsize=(10, 6))
    df['Index'] = df.index
    parallel_coordinates(df, class_column='Index', cols=['overlap_accuracy', 'proximity_accuracy', 'partial_match_accuracy'], color=cm.rainbow(np.linspace(0, 1, len(df))))
    plt.title('Parallel Coordinates Plot of Accuracy Metrics')
    plt.xlabel('Metric')
    plt.ylabel('Accuracy')
    plt.savefig('Evaluation/Retrieve/Plots/parallel_coordinates.png')
    plt.close()

def create_precision_recall_f1_plot(df: pd.DataFrame) -> None:
    """
    Creates and saves a plot of precision, recall, and F1 score across all queries.

    Parameters:
        df (pd.DataFrame): DataFrame containing the precision, recall, and F1 score metrics.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['precision'], label='Precision', color='blue', marker='o')
    plt.plot(df.index, df['recall'], label='Recall', color='green', marker='o')
    plt.plot(df.index, df['f1_score'], label='F1 Score', color='red', marker='o')
    plt.title('Precision, Recall, and F1 Score')
    plt.xlabel('Query Index')
    plt.ylabel('Score')
    plt.legend()
    plt.savefig('Evaluation/Retrieve/Plots/precision_recall_f1_plot.png')
    plt.close()

def create_mrr_plot(df: pd.DataFrame) -> None:
    """
    Creates and saves a plot of Mean Reciprocal Rank (MRR) across all queries.

    Parameters:
        df (pd.DataFrame): DataFrame containing the MRR scores.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['mrr'], label='MRR', color='purple', marker='o')
    plt.title('Mean Reciprocal Rank (MRR)')
    plt.xlabel('Query Index')
    plt.ylabel('MRR Score')
    plt.legend()
    plt.savefig('Evaluation/Retrieve/Plots/mrr_plot.png')
    plt.close()

def main() -> None:
    """
    Main function to load the data, clean it, and generate all the plots.
    """
    df = pd.read_csv('Evaluation/Retrieve/Files/accuracy_metrics.csv')
    df['overlap_accuracy'] = pd.to_numeric(df['overlap_accuracy'], errors='coerce')
    df['proximity_accuracy'] = pd.to_numeric(df['proximity_accuracy'], errors='coerce')
    df['partial_match_accuracy'] = pd.to_numeric(df['partial_match_accuracy'], errors='coerce')
    df = df.dropna(subset=['overlap_accuracy', 'proximity_accuracy', 'partial_match_accuracy'])

    os.makedirs('Evaluation/Retrieve/Plots', exist_ok=True)

    create_violin_plot(df)
    create_box_swarm_plot(df)
    create_radar_chart(df)
    create_heatmap(df)
    create_joint_plot(df)
    create_parallel_coordinates_plot(df)
    create_precision_recall_f1_plot(df)
    create_mrr_plot(df)

if __name__ == "__main__":
    main()
