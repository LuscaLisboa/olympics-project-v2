import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame


def _numeric_only(df: pd.DataFrame) -> DataFrame | None:
    """Return a DataFrame containing only numeric columns."""
    if df.empty:
        return df
    return df.select_dtypes(include="number")

def total_plot(df: DataFrame):
    """Return a Fig containing only numeric columns."""
    numeric_df = _numeric_only(df)

    totals = numeric_df.sum(numeric_only=True)

    fig, ax = plt.subplots()
    ax.bar(totals.index, totals.values, edgecolor="black")
    ax.set_title("Total")
    ax.set_xlabel("Columns")
    ax.set_ylabel("Values")
    ax.tick_params(axis="y", rotation=45)

    plt.tight_layout()
    return fig

def histogram_plot(df: DataFrame):
    """Return a Fig containing only numeric columns."""
    numeric_df = _numeric_only(df)

    fig, ax = plt.subplots()
    ax.hist(numeric_df.dropna(), bins=10, edgecolor="black")
    ax.set_title("Histogram")
    ax.set_xlabel("Columns")
    ax.set_ylabel("Values")
    ax.tick_params(axis="y", rotation=45)

    plt.tight_layout()
    return fig