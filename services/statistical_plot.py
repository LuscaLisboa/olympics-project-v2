from __future__ import annotations

from typing import Any, Iterable, Tuple, Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import networkx as nx
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pandas import DataFrame

X_LABEL = {
    "AGE": "years old",
    "HEIGHT": "centimeters",
    "WEIGHT": "kilograms",
    "YEAR": "game year",
}

def _column_label(column: str) -> str:
    """Return a human friendly label for ``column``."""
    return X_LABEL.get(column.upper(), column.title())

def _numeric_only(df: pd.DataFrame | None) -> DataFrame | None:
        """Return a DataFrame containing only numeric columns."""
        if df is None or df.empty:
            return pd.DataFrame()
        return df.select_dtypes(include="number")


class StatisticalPlot:
    """Render plot for statistical summaries of a DataFrame."""
    def __init__(self, df: DataFrame | None, theme_manager: Any | None):
        self.theme_manager = theme_manager
        self.df: DataFrame = df if df is not None else pd.DataFrame()
        self.figures: list[tuple[Figure, Axes]] = []

        if self.theme_manager is not None:
            self.theme_manager.add_observer(self._on_theme_changed)
            self._apply_theme_to_matplotlib()

    def set_dataframe(self, df: DataFrame | None) -> None:
        """Update the DataFrame used to generate the plots."""
        self.df = df if df is not None else pd.DataFrame()
        self.figures.clear()

    def total_plot(self, column: str) -> Figure | None:
        """Create a scatter plot counting the occurrences of *column*."""
        numeric_df = _numeric_only(self.df)
        if column not in numeric_df.columns:
            return None

        all_values = numeric_df[column].dropna()
        if all_values.empty:
            return None

        value_counts = all_values.value_counts().sort_index()

        fig, ax = self._create_figure()
        self._apply_theme_to_figure(fig, ax)
        self.figures.append((fig, ax))

        ax.scatter(value_counts.index, value_counts.values, alpha=0.8)
        ax.scatter(value_counts.index, value_counts.values)

        ax.set_title(column.upper())
        ax.set_xlabel(_column_label(column))
        ax.set_ylabel("Quantity")
        ax.grid(True, linestyle="--")

        fig.tight_layout()
        return fig

    def histogram_plot(self, column: str) -> Figure | None:
        """Create a histogram plot of *column*."""
        numeric_df = _numeric_only(self.df)
        if column not in numeric_df.columns:
            return None

        all_values = numeric_df[column].dropna()
        if all_values.empty:
            return None

        fig, ax = self._create_figure()
        self._apply_theme_to_figure(fig, ax)
        self.figures.append((fig, ax))

        ax.hist(all_values.dropna(), alpha=0.5)
        ax.set_title(column.upper())
        ax.set_xlabel(_column_label(column))
        ax.set_ylabel("Values")
        ax.grid(True, linestyle="--")

        plt.tight_layout()
        return fig

    def percentile_plot(self, column: str) -> Figure | None:
        """Create a percentile plot of *column*."""
        numeric_df = _numeric_only(self.df)
        if column not in numeric_df.columns:
            return None

        all_values = numeric_df[column].dropna()
        if all_values.empty:
            return None

        percentiles = np.linspace(0, 100, 101)
        values = np.percentile(all_values, percentiles)

        fig, ax = plt.subplots()
        self._apply_theme_to_figure(fig, ax)
        self.figures.append((fig, ax))

        ax.plot([p * 100 for p in percentiles], values)
        ax.set_title(column.upper())
        ax.set_xlabel("Percentile %")
        ax.set_ylabel(column)
        ax.grid(True, linestyle="--")

        plt.tight_layout()
        return fig

    def dispersion_plot(self, x_column: str, y_column: str) -> Figure | None:
        """Create a dispersion (scatter) plot for two numeric columns."""
        numeric_df = _numeric_only(self.df)
        if numeric_df.empty:
            return None

        if x_column not in numeric_df.columns or y_column not in numeric_df.columns:
            return None

        values = numeric_df[[x_column, y_column]].dropna()
        if values.empty:
            return None

        sample_size = 10000
        if len(values) > sample_size:
            values = values.sample(sample_size, random_state=42)

        fig, ax = self._create_figure()
        self._apply_theme_to_figure(fig, ax)
        self.figures.append((fig, ax))

        ax.scatter(values[x_column], values[y_column], alpha=0.1)
        ax.set_title(f"{x_column.upper()} × {y_column.upper()}")
        ax.set_xlabel(_column_label(x_column))
        ax.set_ylabel(_column_label(y_column))
        ax.grid(True, linestyle="--")

        plt.tight_layout()
        return fig

    def distribution_plot(self, column: str) -> Figure | None:
        """Create a dispersion (scatter) plot for two numeric columns."""
        numeric_df = _numeric_only(self.df)
        if numeric_df.empty:
            return None

        if column not in numeric_df.columns:
            return None

        fig, ax = self._create_figure()
        self._apply_theme_to_figure(fig, ax)
        self.figures.append((fig, ax))

        ax.hist(numeric_df[column], bins=30, alpha=0.5)
        ax.set_title(f"{column.upper()}")
        ax.set_xlabel(_column_label(column))
        ax.set_ylabel("Count")
        ax.grid(True, linestyle="--")

        plt.tight_layout()
        return fig

    def standard_deviation_plot(self, column: str, group_col: str) -> Figure | None:
        """Create a standard deviation plot for two numeric columns."""
        numeric_df = _numeric_only(self.df)
        if numeric_df.empty:
            return None

        if column not in numeric_df.columns:
            return None

        fig, ax = self._create_figure()
        self._apply_theme_to_figure(fig, ax)
        self.figures.append((fig, ax))

        grouped = numeric_df.groupby(group_col)[column]
        means = grouped.mean()
        stds = grouped.std()

        ax.fill_between(means.index, means - stds, means + stds, alpha=0.4, label='±1σ')
        ax.set_title(f"{column.upper()} — Standard deviation by {group_col}")
        ax.set_xlabel(_column_label(column))
        ax.set_ylabel(_column_label(column))
        ax.grid(True, linestyle="--")

        plt.tight_layout()
        return fig

    def covariance_heatmap_plot(self) -> Figure | None:
        """Create a covariance heatmap plot."""
        numeric_df = _numeric_only(self.df).drop(
            columns=["ID", "Year"], errors="ignore"
        )
        if numeric_df.empty:
            return None

        fig, ax = self._create_figure()
        self._apply_theme_to_figure(fig, ax)
        self.figures.append((fig, ax))

        cov_matrix = numeric_df.cov()

        sns.heatmap(cov_matrix, annot=True, cmap="coolwarm", center=0, fmt=".2f")

        ax.set_title("Covariance Heatmap")
        ax.grid(True, linestyle="--")

        plt.tight_layout()
        return fig

    def correlation_heatmap_plot(self, method: str = "pearson") -> Figure | None:
        """Create a correlation heatmap plot for two numeric columns."""
        numeric_df = _numeric_only(self.df).drop(
            columns=["ID", "Year"], errors="ignore"
        )
        if numeric_df.empty:
            return None

        fig, ax = self._create_figure()
        self._apply_theme_to_figure(fig, ax)
        self.figures.append((fig, ax))

        corr = numeric_df.corr(method=method)

        fig, ax = plt.subplots()
        self._apply_theme_to_figure(fig, ax)
        sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, vmin=-1, vmax=1, ax=ax)
        ax.set_title(f"Correlation Matrix ({method.title()})")
        ax.grid(True, linestyle="--")

        plt.tight_layout()
        return fig

    @staticmethod
    def _create_figure(figure_size: Iterable[float] | None = None) -> Tuple[Figure, Axes]:
        if figure_size is not None:
            fig, ax = plt.subplots(figsize=figure_size)
        else:
            fig, ax = plt.subplots()
        return fig, ax

    def _apply_theme_to_matplotlib(self) -> None:
        if self.theme_manager is None:
            return

        bg = self.theme_manager.get_color("bg")
        text = self.theme_manager.get_color("text_primary")
        plt.rcParams["figure.facecolor"] = bg
        plt.rcParams["axes.facecolor"] = self.theme_manager.get_color("surface")
        plt.rcParams["axes.edgecolor"] = self.theme_manager.get_color("border")
        plt.rcParams["axes.labelcolor"] = text
        plt.rcParams["xtick.color"] = text
        plt.rcParams["ytick.color"] = text
        plt.rcParams["text.color"] = text

    def _apply_theme_to_figure(self, fig: Figure, ax: Axes) -> None:
        if self.theme_manager is None:
            return

        bg = self.theme_manager.get_color("bg")
        surface = self.theme_manager.get_color("surface")
        text = self.theme_manager.get_color("text_primary")

        fig.patch.set_facecolor(bg)
        ax.set_facecolor(surface)
        ax.title.set_color(text)
        ax.xaxis.label.set_color(text)
        ax.yaxis.label.set_color(text)
        ax.tick_params(colors=text)

    def _on_theme_changed(self, *_):
        self._apply_theme_to_matplotlib()
        for fig, ax in self.figures:
            self._apply_theme_to_figure(fig, ax)
            fig.canvas.draw_idle()