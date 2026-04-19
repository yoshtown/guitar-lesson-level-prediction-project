"""
Unit tests for evaluate.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import pytest
from evaluate import compute_scores


LABELS = ["beginner", "intermediate", "advance"]


class TestComputeScores:

    def test_perfect_predictions(self):
        y = ["beginner", "intermediate", "advance"]
        scores = compute_scores(y, y)
        assert scores["accuracy"] == pytest.approx(1.0)
        assert scores["precision"] == pytest.approx(1.0)
        assert scores["recall"] == pytest.approx(1.0)
        assert scores["f1"] == pytest.approx(1.0)

    def test_returns_expected_keys(self):
        y = ["beginner", "beginner"]
        scores = compute_scores(y, y)
        assert set(scores.keys()) == {"accuracy", "precision", "recall", "f1", "confusion_matrix"}

    def test_confusion_matrix_shape(self):
        y_true = ["beginner", "intermediate", "advance"]
        y_pred = ["beginner", "beginner", "advance"]
        scores = compute_scores(y_true, y_pred)
        assert scores["confusion_matrix"].shape == (3, 3)

    def test_accuracy_below_one_on_wrong_predictions(self):
        y_true = ["beginner", "intermediate", "advance"]
        y_pred = ["advance", "beginner", "intermediate"]
        scores = compute_scores(y_true, y_pred)
        assert scores["accuracy"] == pytest.approx(0.0)

    def test_scores_are_floats(self):
        y = ["beginner", "intermediate"]
        scores = compute_scores(y, y)
        for key in ["accuracy", "precision", "recall", "f1"]:
            assert isinstance(scores[key], float)
