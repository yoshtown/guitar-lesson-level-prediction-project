"""
Evaluation utilities for the guitar lesson difficulty classifier.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)
from config import LABELS


def compute_scores(y_true, y_pred, average: str = "weighted") -> dict:
    """
    Compute classification metrics and return them as a dictionary.

    Args:
        y_true: Ground truth labels.
        y_pred: Predicted labels.
        average: Averaging strategy for precision/recall/f1. Default 'weighted'.

    Returns:
        Dict with keys: accuracy, precision, recall, f1, confusion_matrix.
    """
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, average=average),
        "recall": recall_score(y_true, y_pred, average=average),
        "f1": f1_score(y_true, y_pred, average=average),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=LABELS),
    }


def print_scores(y_true, y_pred, labels: list[str] = LABELS) -> None:
    """
    Print classification metrics and display the confusion matrix heatmap.

    Args:
        y_true: Ground truth labels.
        y_pred: Predicted labels.
        labels: Class labels for the confusion matrix axes.
    """
    scores = compute_scores(y_true, y_pred)

    print(f"accuracy:         {scores['accuracy']:.4f}")
    print(f"precision:        {scores['precision']:.4f}")
    print(f"recall:           {scores['recall']:.4f}")
    print(f"f1 (weighted):    {scores['f1']:.4f}")
    print(f"confusion_matrix:\n{scores['confusion_matrix']}")

    show_confusion_matrix(scores["confusion_matrix"], labels)


def show_confusion_matrix(cm, labels: list[str] = LABELS) -> None:
    """
    Render a confusion matrix as a seaborn heatmap.

    Args:
        cm: Confusion matrix array (from sklearn.metrics.confusion_matrix).
        labels: Class labels for axes.
    """
    cm_df = pd.DataFrame(data=cm, index=labels, columns=labels)

    sns.heatmap(cm_df, annot=True, fmt="d", cmap="Blues")
    plt.ylabel("Actual")
    plt.xlabel("Predicted")
    plt.title("Confusion Matrix")
    plt.show()