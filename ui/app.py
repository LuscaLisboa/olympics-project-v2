import tkinter as tk
from tkinter import ttk

from ui.steps.preview_step import PreviewStep


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

        self.step1 = PreviewStep(self.nb)
        self.nb.add(self.step1, text="1 - View File")