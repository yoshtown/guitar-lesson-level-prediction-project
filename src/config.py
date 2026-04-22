"""
Shared constants and configuration for the guitar lesson difficulty classifier.
"""

# Difficulty labels (order matters — beginner < intermediate < advance)
LABELS = ["beginner", "intermediate", "advance"]

# Text features used from the raw dataframe
TEXT_COLUMNS = ["title", "description"]

# TF-IDF best params (from grid search in notebook)
TFIDF_PARAMS = {
    "max_features": 28000,
    "ngram_range": (1, 2),
    "stop_words": None,
}

# MLflow
MLFLOW_EXPERIMENT_NAME = "guitar-lesson-difficulty-classifierv2"

MLFLOW_TRACKING_URI = "https://dagshub.com/yoshtown/guitar-lesson-classifier.mlflow"