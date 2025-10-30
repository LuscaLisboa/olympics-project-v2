import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame


def _numeric_only(df: pd.DataFrame) -> DataFrame | None:
    """Return a DataFrame containing only numeric columns."""
    if df.empty:
        return df
    return df.select_dtypes(include="number")

class StatisticalPlot:
    def __init__(self, df: DataFrame, theme_manager):
        super().__init__()
        self.theme_manager = theme_manager
        self.df = df

        self.theme_manager.add_observer(self._on_theme_changed)

    def total_plot(self, column: str):
        """Group identical values & show count (x=value, y=count) in scatter plot."""
        numeric_df = _numeric_only(self.df)

        all_values = numeric_df[column]

        value_counts = all_values.value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(value_counts.index, value_counts.values, color="steelblue", alpha=0.7, edgecolor="black")

        ax.set_title(column.upper(), fontsize=10)
        ax.set_xlabel("", color="red")
        ax.set_ylabel("Quantity")
        ax.grid(True, linestyle="--", alpha=0.4)

        plt.tight_layout()
        return fig

    def histogram_plot(self):
        """Return a Fig containing only numeric columns."""
        numeric_df = _numeric_only(self.df)

        fig, ax = plt.subplots()
        ax.hist(numeric_df.dropna(), edgecolor="black")
        ax.set_title("Histogram")
        ax.set_xlabel("Columns")
        ax.set_ylabel("Values")
        ax.tick_params(axis="y", rotation=45)

        plt.tight_layout()
        return fig

    def _update_canvas_color(self, canvas):
        if self.theme_manager:
            canvas.configure(bg=self.theme_manager.get_color("bg"))

    def _on_theme_changed(self):
        self._update_canvas_color(self.canvas)