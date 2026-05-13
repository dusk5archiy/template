from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np


def calc_classification_metrics(targets: np.ndarray, preds: np.ndarray):
    """
    Calculates classification metrics, including precision, recall and f1score.

    Args:
        targets (np.ndarray): Array of target values.
        preds (np.ndarray): Array of predicted values.

    Returns:
        tuple[int, int, int]: All the metrics mentioned.
    """
    precision = precision_score(targets, preds, average="weighted")
    recall = recall_score(targets, preds, average="weighted")
    f1 = f1_score(targets, preds, average="weighted")

    precision = float(precision)
    recall = float(recall)
    f1 = float(f1)

    return precision, recall, f1
