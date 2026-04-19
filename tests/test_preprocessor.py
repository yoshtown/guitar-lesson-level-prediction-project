"""
Unit tests for preprocessor.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandas as pd
import pytest
from preprocessor import combine_text_features


def make_df(**kwargs):
    return pd.DataFrame(kwargs)


class TestCombineTextFeatures:

    def test_basic_combination(self):
        df = make_df(title=["Beginner Chords"], description=["Easy open chords tutorial"])
        result = combine_text_features(df)
        assert result[0] == "Beginner Chords Easy open chords tutorial"

    def test_multiple_rows(self):
        df = make_df(
            title=["Beginner Chords", "Advanced Solo"],
            description=["Easy open chords", "Shred techniques"],
        )
        result = combine_text_features(df)
        assert len(result) == 2
        assert result[1] == "Advanced Solo Shred techniques"

    def test_returns_series(self):
        df = make_df(title=["A"], description=["B"])
        result = combine_text_features(df)
        assert isinstance(result, pd.Series)

    def test_missing_column_raises(self):
        df = make_df(title=["A"])  # missing 'description'
        with pytest.raises(ValueError, match="missing expected columns"):
            combine_text_features(df)

    def test_custom_columns(self):
        df = make_df(title=["A"], description=["B"], tags=["C"])
        result = combine_text_features(df, columns=["title", "tags"])
        assert result[0] == "A C"

    def test_nan_handled_as_string(self):
        """NaN values in text columns should not raise — they become the string 'nan'."""
        df = make_df(title=["Beginner Chords"], description=[None])
        result = combine_text_features(df)
        assert isinstance(result[0], str)
        assert "Beginner Chords" in result[0]
