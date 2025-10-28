import tkinter as tk
from tkinter import ttk

import pandas

from ui.steps.preview_step import GetDataStep
from ui.steps.statistics_step import StatisticsStep


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self._build()

    def _build(self):
        container = tk.Frame(self.root, padx=8, pady=8)
        container.pack(fill="both", expand=True)

        title = ttk.Label(container, text="Olympics Analysis", font=("Segoe UI", 16, "bold"))
        title.pack(anchor="w", pady=(0,8))

        self.nb = ttk.Notebook(container)
        self.nb.pack(fill="both", expand=True)

        self.step1 = GetDataStep(self.nb)
        self.nb.add(self.step1, text="1 - View File")

        self.step2 = StatisticsStep(self.nb, self.step1.df if self.step1.df else pandas.DataFrame(), self.step1.file_label_var)
        self.nb.add(self.step2, text="2 - Statistics")

