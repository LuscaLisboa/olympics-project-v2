import tkinter as tk
from tkinter import ttk

import pandas

from ui.steps.get_data_step import GetDataStep
from ui.steps.statistical_step import StatisticsStep
from ui.theme.theme_manager import ThemeManager


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.theme_manager = ThemeManager(root, initial_theme="light")
        self._build()

    def _build(self):
        container = tk.Frame(self.root,bg=self.theme_manager.get_color("bg"))
        container.pack(fill="both", expand=True)

        top_bar = ttk.Frame(container)
        top_bar.pack(fill="x")

        title = ttk.Label(top_bar, text="Olympics Analysis", style="TLabel")
        title.grid(column=0, row=0, sticky="w")

        toggle_btn = ttk.Button(
            top_bar,
            text="Theme",
            command=self.theme_manager.cycle_theme,
            style="TButton",
        )
        toggle_btn.grid(row=0, column=1, sticky="e")

        top_bar.columnconfigure(0, weight=1)

        self.nb = ttk.Notebook(container, style="TNotebook")
        self.nb.pack(fill="both", expand=True)

        self.step1 = GetDataStep(self.nb, self.theme_manager)
        self.nb.add(self.step1, text="1 - View File")

        self.step2 = StatisticsStep(self.nb, self.step1.df if self.step1.df else pandas.DataFrame(), self.step1.file_label_var, theme_manager=self.theme_manager)
        self.nb.add(self.step2, text="2 - Statistics")
        self.step1.on_data_loaded = self._on_data_loaded

    def _on_data_loaded(self, df: pandas.DataFrame, _meta: dict):
        self.step2.update_dataframe(df)