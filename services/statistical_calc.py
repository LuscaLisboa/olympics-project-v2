import pandas as pd
from pandas import DataFrame


def _numeric_only(df: pd.DataFrame) -> DataFrame | None:
    """Return a DataFrame containing only numeric columns."""
    if df.empty:
        return df
    return df.select_dtypes(include="number")

def total_calc(df: pd.DataFrame) -> dict[str, int]:
    """Return the sum of numeric values within each column of ``df``."""
    numeric_df = _numeric_only(df)
    if numeric_df.empty:
        return {}
    return numeric_df.sum(numeric_only=True).to_dict()

def average_calc(df: pd.DataFrame) -> dict[str, int]:
    """Return the average of numeric values within each column of ``df``."""
    numeric_df = _numeric_only(df)
    if numeric_df.empty:
        return {}
    return numeric_df.mean(numeric_only=True).to_dict()

def median_calc(df: pd.DataFrame) -> dict[str, int]:
    """Return the median of numeric values within each column of ``df``."""
    numeric_df = _numeric_only(df)
    if numeric_df.empty:
        return {}
    return numeric_df.median(numeric_only=True).to_dict()

def mode_calc(df: pd.DataFrame) -> dict[str, int]:
    """Return the mode of numeric values within each column of ``df``."""
    numeric_df = _numeric_only(df)
    if numeric_df.empty:
        return {}
    return numeric_df.mode(numeric_only=True).to_dict()

def variance_calc(df: pd.DataFrame) -> dict[str, int]:
    """Return the variance of numeric values within each column of ``df``."""
    numeric_df = _numeric_only(df)
    if numeric_df.empty:
        return {}
    return numeric_df.var(numeric_only=True).to_dict()

def std_deviation_calc(df: pd.DataFrame) -> dict[str, int]:
    """Return the standard deviation of numeric values within each column of ``df``."""
    numeric_df = _numeric_only(df)
    if numeric_df.empty:
        return {}
    return numeric_df.std(numeric_only=True).to_dict()

def covariance_calc(df: pd.DataFrame) -> dict[str, int]:
    """Return the covariance of numeric values within each column of ``df``."""
    numeric_df = _numeric_only(df)
    if numeric_df.empty:
        return {}
    return numeric_df.cov(numeric_only=True).to_dict()

def correlation_calc(df: pd.DataFrame) -> dict[str, int]:
    """Return the correlation of numeric values within each column of ``df``."""
    numeric_df = _numeric_only(df)
    if numeric_df.empty:
        return {}
    return numeric_df.corr(numeric_only=True).to_dict()