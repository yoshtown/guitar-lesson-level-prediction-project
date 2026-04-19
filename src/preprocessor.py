"""
Text preprocessing for the guitar lesson difficulty classifier.

Responsibility: take raw dataframe rows and produce a single
combined text string ready for TF-IDF vectorization.
"""

import pandas as pd
from config import TEXT_COLUMNS
from sklearn.feature_extraction.text import TfidfVectorizer
from config import LABELS, MLFLOW_EXPERIMENT_NAME, TFIDF_PARAMS, TEXT_COLUMNS

def combine_text_features(df: pd.DataFrame, columns: list[str] = TEXT_COLUMNS) -> pd.Series:
    """
    Concatenate multiple text columns into a single space-separated string per row.

    Args:
        df: DataFrame containing the raw video data.
        columns: List of column names to combine. Defaults to TEXT_COLUMNS from config.

    Returns:
        A Series of combined text strings, one per row.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({"title": ["Beginner Chords"], "description": ["Easy open chords"]})
        >>> combine_text_features(df)
        0    Beginner Chords Easy open chords
        dtype: object
    """
    missing_columns = [column for column in columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"DataFrame is missing expected columns: {missing_columns}")

    return df[columns].fillna("").apply(lambda row: " ".join(row.astype(str)), axis=1)

def build_tfidf_features(
    X_train: pd.Series,
    X_val: pd.Series,
    tfidf_params: dict = TFIDF_PARAMS,
):
    """
    Fit a TF-IDF vectorizer on training data and transform both splits.

    Args:
        X_train: Training text Series.
        X_val: Validation text Series.
        tfidf_params: Keyword args passed to TfidfVectorizer.

    Returns:
        Tuple of (vectorizer, X_train_tfidf, X_val_tfidf).
    """
    vectorizer = TfidfVectorizer(**tfidf_params)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_val_tfidf = vectorizer.transform(X_val)

    return vectorizer, X_train_tfidf, X_val_tfidf
