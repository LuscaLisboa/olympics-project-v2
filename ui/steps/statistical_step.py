import tkinter as tk
from tkinter import ttk

import pandas as pd

from services.statistical_calc import total_calc, average_calc


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
        ttk.Label(top, textvariable=self.label).pack(side="left", padx=12)

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True)

        #   Iter per 'calc' & generate notebook sheets with cards inside 'df.columns'
        for calc in _calc():
            self._build_calc_sheet(calc, self.df.columns)

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
            ).pack(expand=True)
            self.nb.add(frame, text="Info")
            self._notify("No data loaded.")
            return
        for calc in self._calcs:
            self._build_calc_sheet(calc, self.df.columns)

        self._notify(f"{len(self.df.columns)} columns loaded.")

    def _build_calc_sheet(self, calc_name: str, df_columns):
        frame = ttk.Frame(self.nb, padding=8)
        self.nb.add(frame, text=str(calc_name))
        self.tabs_by_calc[calc_name] = frame

        cards = ttk.Frame(frame)
        cards.pack(fill="x", pady=(8, 0))

        grid_length = 5
        for i in range(grid_length):
            cards.grid_columnconfigure(i, weight=1)

        results = {}
        match calc_name:
            case "Total":
                results = total_calc(self.df)
            case "Average":
                results = average_calc(self.df)

        for idx, col in enumerate(df_columns):
            r, c = divmod(idx, grid_length)
            lf = ttk.LabelFrame(cards, text=col, padding=10)
            lf.grid(row=r, column=c, sticky="nsew", padx=6, pady=6)
            if col in results:
                ttk.Label(lf, text=results[col], font=("Segoe UI", 14, "bold")).grid(
                    row=0, column=0, sticky="nsew"
                )