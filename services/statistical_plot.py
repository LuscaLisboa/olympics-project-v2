import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame


def _numeric_only(df: pd.DataFrame) -> DataFrame | None:
    """Return a DataFrame containing only numeric columns."""
    if df.empty:
        return df
    return df.select_dtypes(include="number")

def total_plot(df: DataFrame, column: str):
    """Group identical values & show count (x=value, y=count) in scatter plot."""
    numeric_df = df.select_dtypes(include="number")

    all_values = numeric_df[column].stack()

    value_counts = all_values.value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(value_counts.index, value_counts.values, color="steelblue", alpha=0.7, edgecolor="black")

    ax.set_title(column.upper())
    ax.set_xlabel(all_values)
    ax.set_ylabel("count")
    ax.grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()
    return fig

def histogram_plot(df: DataFrame):
    """Return a Fig containing only numeric columns."""
    numeric_df = _numeric_only(df)

    fig, ax = plt.subplots()
    ax.hist(numeric_df.dropna(), edgecolor="black")
    ax.set_title("Histogram")
    ax.set_xlabel("Columns")
    ax.set_ylabel("Values")
    ax.tick_params(axis="y", rotation=45)

    plt.tight_layout()
    return fig