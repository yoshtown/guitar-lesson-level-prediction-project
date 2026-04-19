"""
Training utilities for the guitar lesson difficulty classifier.

Contains the reusable MLflow run wrapper (start_ml_run) and
data loading / splitting helpers.
"""

import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, confusion_matrix

from config import LABELS, MLFLOW_EXPERIMENT_NAME, TFIDF_PARAMS, TEXT_COLUMNS
from evaluate import compute_scores
from preprocessor import combine_text_features

# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def load_data(data_path: str | Path) -> pd.DataFrame:
    """
    Load the raw guitar lesson dataset from a parquet file/folder.

    Args:
        data_path: Path to the parquet file or directory.

    Returns:
        Raw DataFrame.
    """
    return pd.read_parquet(data_path)


def prepare_splits(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple:
    """
    Build text features and split into train/validation sets.

    Args:
        df: Raw DataFrame containing TEXT_COLUMNS and 'level' column.
        test_size: Proportion of data to use for validation.
        random_state: Reproducibility seed.

    Returns:
        Tuple of (X_train, X_val, y_train, y_val) where X is a Series of strings.
    """
    X = combine_text_features(df)
    y = df["level"]
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

# ---------------------------------------------------------------------------
# MLflow run wrapper
# ---------------------------------------------------------------------------

def start_ml_run(
    model,
    run_name: str,
    params: dict,
    X_train,
    X_val,
    y_train,
    y_val,
    encoder=None,
    register: bool = False,
    registered_model_name: str = "guitar-lesson-difficulty-classifier",
) -> dict:
    """
    Train a model and log everything to MLflow in a single run.

    Args:
        model: An unfitted sklearn-compatible estimator.
        run_name: Human-readable label for this MLflow run.
        params: Dict of hyperparameters to log.
        X_train: Training features (sparse matrix or array).
        X_val: Validation features.
        y_train: Training labels.
        y_val: Validation labels.
        encoder: Optional LabelEncoder — if provided, inverse-transforms predictions.
        register: If True, registers the model in the MLflow Model Registry.
        registered_model_name: Name to use in the registry when register=True.

    Returns:
        Dict of computed evaluation metrics.
    """
    with mlflow.start_run(run_name=run_name):
        # --- Train ---
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)

        if encoder:
            y_pred = encoder.inverse_transform(y_pred)

        # --- Metrics ---
        scores = compute_scores(y_val, y_pred)

        mlflow.log_params(params)
        mlflow.log_metric("accuracy", scores["accuracy"])
        mlflow.log_metric("precision", scores["precision"])
        mlflow.log_metric("recall", scores["recall"])
        mlflow.log_metric("f1_weighted", scores["f1"])

        # --- Confusion matrix artifact ---
        fig, ax = plt.subplots(figsize=(6, 4))
        ConfusionMatrixDisplay.from_predictions(y_val, y_pred, ax=ax)
        plt.tight_layout()
        mlflow.log_figure(fig, "confusion_matrix.png")
        plt.close()

        if isinstance(model, XGBClassifier):
            mlflow.xgboost.log_model(model, artifact_path="model")
        else:
            mlflow.sklearn.log_model(model, artifact_path="model")

        # --- Model artifact (+ optional registry) ---
        if register:
        	log_kwargs = {"artifact_path": "model", "registered_model_name": registered_model_name}
    	else:
    		log_kwargs = {"artifact_path": "model"}

		if isinstance(model, XGBClassifier):
    		mlflow.xgboost.log_model(model, **log_kwargs)
		else:
	        mlflow.sklearn.log_model(model, **log_kwargs)

    return scores