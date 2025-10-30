import tkinter as tk
from tkinter import ttk
from typing import Any, Mapping

import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from services.statistical_calc import (
    average_calc,
    correlation_calc,
    covariance_calc,
    median_calc,
    mode_calc,
    std_deviation_calc,
    total_calc,
    variance_calc,
)
from services.statistical_plot import total_plot, histogram_plot


def _calc():
    return [
        "Total",
        "Average",
        "Median",
        "Mode",
        "Variance",
        "Standard Deviation",
        "Covariance",
        "Correlation",
    ]


class StatisticsStep(ttk.Frame):
    def __init__(self, parent, df: pd.DataFrame | None, label, *args, **kwargs):
        super().__init__(parent, *args, **kwargs, padding=8)

        if not isinstance(label, tk.StringVar):
            label = tk.StringVar(value="")
        self.label = label

        self.on_status = None
        self.df: pd.DataFrame = df if df is not None else pd.DataFrame()
        self.tabs_by_calc: dict[str, ttk.Frame] = {}
        self._calcs = _calc()

        self._build()
        self.update_dataframe(self.df)

    def _notify(self, msg: str):
        if self.on_status:
            self.on_status(msg)

    def _build(self):
        top = ttk.Frame(self)
        top.pack(fill="x", pady=(0,8))
        ttk.Label(top, textvariable=self.label, style="Info.TLabel").pack(side="left", padx=12)

        self.nb = ttk.Notebook(self, style="TNotebook")
        self.nb.pack(fill="both", expand=True)

        self._notify(f"{len(self.df.columns)} columns loaded.")

    def update_dataframe(self, df: pd.DataFrame | None):
        self.df = df if df is not None else pd.DataFrame()

        for tab_id in self.nb.tabs():
            self.nb.forget(tab_id)
        self.tabs_by_calc.clear()

        if self.df.empty or len(self.df.columns) == 0:
            frame = ttk.Frame(self.nb, padding=16)
            ttk.Label(
                frame,
                text="Load a file in Step 1 to view available columns.",
                anchor="center",
                justify="center",
                style="Info.TLabel"
            ).pack(expand=True)
            self.nb.add(frame, text="Info")
            self._notify("No data loaded.")
            return

        numeric_df = self.df.select_dtypes(include="number").drop(
            columns=["ID"], errors="ignore"
        )
        numeric_columns = list(numeric_df.columns)

        if len(numeric_columns) == 0:
            frame = ttk.Frame(self.nb, padding=16)
            ttk.Label(
                frame,
                text=(
                    "No numeric columns available. Update the dataset to view statistics."
                ),
                anchor="center",
                justify="center",
            ).pack(expand=True)
            self.nb.add(frame, text="Info")
            self._notify("No numeric data available.")
            return

        calc_results: dict[str, Any] = {}
        plots_by_calc: dict[str, list] = {}
        for calc in self._calcs:
            match calc:
                case "Total":
                    calc_results[calc] = total_calc(numeric_df)
                    for c in numeric_columns:
                        plots_by_calc.setdefault(calc, []).append(total_plot(numeric_df, c))
                case "Average":
                    calc_results[calc] = average_calc(numeric_df)
                    plots_by_calc[calc] = histogram_plot(numeric_df)
                case "Median":
                    calc_results[calc] = median_calc(numeric_df)
                    plots_by_calc[calc] = {}
                case "Mode":
                    calc_results[calc] = mode_calc(numeric_df)
                    plots_by_calc[calc] = {}
                case "Variance":
                    calc_results[calc] = variance_calc(numeric_df)
                    plots_by_calc[calc] = {}
                case "Standard Deviation":
                    calc_results[calc] = std_deviation_calc(numeric_df)
                    plots_by_calc[calc] = {}
                case "Covariance":
                    calc_results[calc] = covariance_calc(numeric_df)
                    plots_by_calc[calc] = {}
                case "Correlation":
                    calc_results[calc] = correlation_calc(numeric_df)
                    plots_by_calc[calc] = {}
                case _:
                    calc_results[calc] = {}

        for calc in self._calcs:
            self._build_calc_sheet(
                calc,
                numeric_columns,
                calc_results.get(calc, {}),
                plots_by_calc.get(calc),
            )

        self._notify(f"{len(numeric_columns)} numeric columns loaded.")

    @staticmethod
    def _format_result(value: Any) -> str:
        if isinstance(value, Mapping):
            lines = []
            for key, val in value.items():
                rendered = StatisticsStep._format_result(val)
                if "\n" in rendered:
                    lines.append(f"{key}:\n{rendered}")
                else:
                    lines.append(f"{key}: {rendered}")
            return "\n".join(lines)
        if isinstance(value, (list, tuple, set)):
            return "\n".join(StatisticsStep._format_result(item) for item in value)
        if value is None:
            return "—"
        return str(value)

    def _add_plot(self, parent, figs):
        if figs is None:
            return
        if not isinstance(figs, (list, tuple)):
            figs = [figs]

        rows = (len(figs) + 1)
        for i in range(rows):
            parent.grid_rowconfigure(i, weight=1)
        for j in range(2):
            parent.grid_columnconfigure(j, weight=1)

        for idx, fig in enumerate(figs):
            if fig is None:
                continue
            r, c = divmod(idx, 2)
            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas.draw()
            canvas.get_tk_widget().grid(row=r, column=c, sticky="nsew", padx=8, pady=8)

    def _build_calc_sheet(
            self,
            calc_name: str,
            df_columns,
            results: Mapping[str, Any] | None,
            figure: Any,
    ):
        frame = ttk.Frame(self.nb, padding=4)
        self.nb.add(frame, text=str(calc_name))
        self.tabs_by_calc[calc_name] = frame

        cards = ttk.Frame(frame)
        cards.pack(fill="x", pady=(8, 0))

        grid_length = 4
        for i in range(grid_length):
            cards.grid_columnconfigure(i, weight=1)

        for idx, col in enumerate(df_columns):
            r, c = divmod(idx, grid_length)
            lf = ttk.LabelFrame(cards, text=col)
            lf.grid(row=r, column=c, sticky="nsew")
            if results and col in results:
                text = self._format_result(results[col])
                ttk.Label(
                    lf,
                    text=text,
                    justify="left",
                    anchor="w",
                    style="Info.TLabel",
                ).grid(row=0, column=0, sticky="nsew")
        if figure is not None:
            plot_frame = ttk.Frame(frame)
            plot_frame.pack(fill="both", expand=True, pady=(10, 0))
            self._add_plot(plot_frame, figure)