import pandas as pd


def compute_overlap_accuracy(row: pd.Series) -> float:
    """
    Computes overlap-based accuracy for a given row in the DataFrame.

    Parameters:
        row (pd.Series): A row of the DataFrame containing 'expected top-k chunks to be searched'
                         and 'Top-K searched chunks'.

    Returns:
        float: The accuracy calculated as the intersection of the top-k chunks and expected chunks
               divided by the number of expected chunks.
    """
    expected_chunks = eval(row['expected top-k chunks to be searched'])
    top_k_chunks = eval(row['Top-K searched chunks'])
    intersection = set(top_k_chunks).intersection(set(expected_chunks))
    accuracy = len(intersection) / len(expected_chunks) if expected_chunks else 0
    return accuracy

def compute_proximity_accuracy(row: pd.Series) -> float:
    """
    Computes proximity-based accuracy for a given row in the DataFrame.

    Parameters:
        row (pd.Series): A row of the DataFrame containing 'expected top-k chunks to be searched'
                         and 'Top-K searched chunks'.

    Returns:
        float: The accuracy calculated based on the proximity of the top-k chunks to the expected chunks.
               Closer matches get higher scores, normalized by the number of expected chunks.
    """
    top_k_chunks = eval(row['Top-K searched chunks'])
    expected_chunks = eval(row['expected top-k chunks to be searched'])
    if not expected_chunks:
        return 0
    proximity_sum = 0
    for chunk in top_k_chunks:
        min_distance = min([abs(chunk - expected_chunk) for expected_chunk in expected_chunks])
        proximity_sum += 1 / (1 + min_distance)
    proximity_accuracy = proximity_sum / len(expected_chunks)
    return proximity_accuracy

def compute_partial_match_accuracy(row: pd.Series) -> float:
    """
    Computes partial match accuracy for a given row in the DataFrame.

    Parameters:
        row (pd.Series): A row of the DataFrame containing 'expected top-k chunks to be searched'
                         and 'Top-K searched chunks'.

    Returns:
        float: The accuracy calculated by checking for exact matches and close matches.
               Partial credit is given for close matches, normalized by the number of expected chunks.
    """
    top_k_chunks = eval(row['Top-K searched chunks'])
    expected_chunks = eval(row['expected top-k chunks to be searched'])
    if not expected_chunks:
        return 0
    partial_match_sum = 0
    for chunk in top_k_chunks:
        if chunk in expected_chunks:
            partial_match_sum += 1
        else:
            min_distance = min([abs(chunk - expected_chunk) for expected_chunk in expected_chunks])
            if min_distance == 1:
                partial_match_sum += 0.5
    partial_match_accuracy = partial_match_sum / len(expected_chunks)
    return partial_match_accuracy

def compute_metrics(row: pd.Series) -> pd.Series:
    """
    Computes precision, recall, F1 score, and Mean Reciprocal Rank (MRR) for a given row in the DataFrame.

    Parameters:
        row (pd.Series): A row of the DataFrame containing 'expected top-k chunks to be searched'
                         and 'Top-K searched chunks'.

    Returns:
        pd.Series: A series containing the precision, recall, F1 score, and MRR.
    """
    expected_chunks = set(eval(row['expected top-k chunks to be searched']))
    top_k_chunks = set(eval(row['Top-K searched chunks']))

    true_positive = len(expected_chunks.intersection(top_k_chunks))
    false_positive = len(top_k_chunks - expected_chunks)
    precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0

    recall = true_positive / len(expected_chunks) if expected_chunks else 0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0

    mrr = 0
    for rank, chunk in enumerate(eval(row['Top-K searched chunks']), start=1):
        if chunk in expected_chunks:
            mrr = 1 / rank
            break

    return pd.Series([precision, recall, f1_score, mrr])

df = pd.read_csv('Evaluation/Retrieve/Files/all_chunks.csv')

df['overlap_accuracy'] = df.apply(compute_overlap_accuracy, axis=1)
df['proximity_accuracy'] = df.apply(compute_proximity_accuracy, axis=1)
df['partial_match_accuracy'] = df.apply(compute_partial_match_accuracy, axis=1)

df[['precision', 'recall', 'f1_score', 'mrr']] = df.apply(compute_metrics, axis=1)

result = df[['Question', 'overlap_accuracy', 'proximity_accuracy', 'partial_match_accuracy', 'precision', 'recall', 'f1_score', 'mrr']]
result.to_csv('Evaluation/Retrieve/Files/accuracy_metrics.csv', index=False)
