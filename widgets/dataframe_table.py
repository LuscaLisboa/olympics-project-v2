import tkinter as tk
from tkinter import ttk

import pandas as pd

class DataFrameTable(ttk.Frame):
    def __init__(self, master, theme_manager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.theme_manager = theme_manager
        self.tree = None

        self._build()
        self.theme_manager.add_observer(self._on_theme_changed)

    def _build(self):
        self.tree = ttk.Treeview(self, show="headings", style="Treeview")
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def set_dataframe(self, df: pd.DataFrame):
        #   Clear
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")
            self.tree.column(col, width=0)
        self.tree.delete(*self.tree.get_children())

        #   Set
        columns = [str(c) for c in df.columns]
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=min(max(80, len(col) * 10), 400), stretch=True, anchor="w")

        if not df.empty:
            values_iter = df.itertuples(index=False, name=None)
            batch = []
            for i, row in enumerate(values_iter, start=1):
                batch.append(row)
                if len(batch) >= 1000:
                    for r in batch:
                        self.tree.insert("", "end", values=r)
                    batch.clear()
            for r in batch:
                self.tree.insert("", "end", values=r)

    def _update_canvas_color(self, canvas):
        if self.theme_manager:
            canvas.configure(bg=self.theme_manager.get_color("bg"))

    def _on_theme_changed(self):
        self._update_canvas_color(self.canvas)