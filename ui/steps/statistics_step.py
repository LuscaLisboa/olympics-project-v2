import tkinter as tk
from tkinter import ttk

import pandas as pd


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
    def __init__(self, parent, df: pd.DataFrame, label, *args, **kwargs):
        super().__init__(parent, *args, **kwargs, padding=8)

        if not isinstance(label, tk.StringVar):
            label = tk.StringVar(value="")
        self.label = label

        self.on_status = None
        self.df: pd.DataFrame = df
        self.tabs_by_calc: dict[str, ttk.Frame] = {}

        self._build()

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

    def _notify(self, msg: str):
        if self.on_status:
            self.on_status(msg)



    def _build_calc_sheet(self, calc_name: str, df_columns):
        frame = ttk.Frame(self.nb, padding=8)
        self.nb.add(frame, text=str(calc_name))
        self.tabs_by_calc[calc_name] = frame

        cards = ttk.Frame(frame)
        cards.pack(fill="x", pady=(8, 0))

        # layout responsivo (3 colunas)
        for i in range(3):
            cards.grid_columnconfigure(i, weight=1)

        cards_specs = []
        for col in df_columns:
            cards_specs.append((col, "—"))

        for idx, col in enumerate(df_columns):
            r, c = divmod(idx, 3)
            lf = ttk.LabelFrame(cards, text=col, padding=10)
            lf.grid(row=r, column=c, sticky="nsew", padx=6, pady=6)
            ttk.Label(lf, text="—", font=("Segoe UI", 14, "bold")).grid(
                row=0, column=0, sticky="nsew"
            )