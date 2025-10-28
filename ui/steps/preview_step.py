import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import pandas as pd

from services.io_loader import load_table
from widgets.dataframe_table import DataFrameTable


class PreviewStep(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)
        self.on_status = None
        self.df: pd.DataFrame | None = None
        self.page_idx = 0
        self.page_size = 500

        self._build()

    def _build(self):
        bar = ttk.Frame(self)
        bar.pack(fill="x", pady=(0,8))

        self.btn_open = ttk.Button(bar, text="Open file", command=self._open_file)
        self.btn_open.pack(side="left")

        self.file_label_var = tk.StringVar(value="No file selected")
        ttk.Label(bar, textvariable=self.file_label_var).pack(side="left", padx=12)

        bar2 = ttk.Frame(self)
        bar2.pack(fill="x", pady=(0,4))

        self.page_info = tk.StringVar(value="—")
        self.btn_prev = ttk.Button(bar2, text="◀ Previous", command=self._prev_page, state="disabled")
        self.btn_next = ttk.Button(bar2, text="Next ▶", command=self._next_page, state="disabled")
        self.btn_prev.pack(side="left")
        self.btn_next.pack(side="right")
        ttk.Label(bar2, textvariable=self.page_info).pack(side="left", padx=12)

        self.table = DataFrameTable(self)
        self.table.pack(fill="both", expand=True)

    def _open_file(self):
        fp = filedialog.askopenfilename(
            title="Select file",
            filetypes=[("Sheets", "*.xlsx *xls *.csv"), ("All files", "*.*")]
        )
        if not fp:
            return
        try:
            self._notify("Loading...")
            self.df, meta = load_table(fp, sample_rows=None)
            self.file_label_var.set(f"File: {meta['name']}  •  Rows: {meta['rows']}  •  Columns: {meta['cols']}")
            self.page_idx = 0
            self._render_page()
            self._notify("Loading successfully")
        except Exception as e:
            messagebox.showerror("Error while opening", str(e))
            self._notify("Loading error")

    def _notify(self, msg: str):
        if self.on_status:
            self.on_status(msg)

    def _render_page(self):
        if self.df is None:
            return
        total = len(self.df)
        start = self.page_idx * self.page_size
        end = min(start + self.page_size, total)

        if start >= total > 0:
            self.page_idx = max((total - 1) // self.page_size, 0)
            start = self.page_idx * self.page_size
            end = min(start + self.page_size, total)

        page_df = self.df.iloc[start:end].reset_index(drop=True)
        self.table.set_dataframe(page_df)
        self.page_info.set(f"Showing {start+1}-{end} of {total} rows (page {self.page_idx+1}/{max((total-1)//self.page_size+1, 1)})")

        if total == 0:
            self.btn_prev.config(state="disabled")
            self.btn_next.config(state="disabled")
        else:
            self.btn_prev.config(state="normal" if self.page_idx > 0 else "disabled")
            self.btn_next.config(state="normal" if end < total else "disabled")


    def _prev_page(self):
        if self.df is None:
            return
        if self.page_idx > 0:
            self.page_idx -= 1
        self._render_page()

    def _next_page(self):
        if self.df is None:
            return
        self.page_idx += 1
        self._render_page()