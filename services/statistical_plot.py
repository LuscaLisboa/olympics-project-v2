from __future__ import annotations

from typing import Any, Iterable, Tuple

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pandas import DataFrame

X_LABEL = {
    "AGE": "years old",
    "HEIGHT": "centimeters",
    "WEIGHT": "kilograms",
    "YEAR": "game year"
}

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
        self.figures = []

        if self.theme_manager is not None:
            self.theme_manager.add_observer(self._on_theme_changed)
            self._apply_theme_to_matplotlib()

    def set_dataframe(self, df: DataFrame | None) -> None:
        """Update the DataFrame used to generate the plots."""
        self.df = df if df is not None else pd.DataFrame()

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

        ax.scatter(value_counts.index,value_counts.values)
        ax.scatter(value_counts.index, value_counts.values)

        ax.set_title(column.upper())
        ax.set_xlabel(X_LABEL.get(column))
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

        fig, ax = plt.subplots()
        self._apply_theme_to_figure(fig, ax)
        self.figures.append((fig, ax))

        ax.hist(all_values.dropna())
        ax.set_title(column.upper())
        ax.set_xlabel(X_LABEL.get(column))
        ax.set_ylabel("Values")
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