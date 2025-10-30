import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional, Callable

import pandas as pd

from services.io_loader import load_table
from widgets.dataframe_table import DataFrameTable


class GetDataStep(ttk.Frame):
    def __init__(self, master, theme_manager):
        super().__init__(master, padding=8)
        self.theme_manager = theme_manager
        self.on_status = None
        self.df: pd.DataFrame | None = None
        self.page_idx = 0
        self.page_size = 500
        self.on_data_loaded: Optional[Callable[[pd.DataFrame, dict], None]] = None

        self._build()
        self.theme_manager.add_observer(self._on_theme_changed)

    def _build(self):
        colors = self.theme_manager.get_all_colors()

        bar = ttk.Frame(self, style="TFrame")
        bar.pack(fill="x", pady=(0,8))

        self.btn_open = ttk.Button(bar, text="Open file", command=self._open_file, style="TButton")
        self.btn_open.pack(side="left")

        self.file_label_var = tk.StringVar(value="No file selected")
        ttk.Label(bar, textvariable=self.file_label_var, style="Info.Label").pack(side="left", padx=12)

        bar2 = ttk.Frame(self, style="Card.TFrame")
        bar2.pack(fill="x", pady=(0,4))

        self.page_info = tk.StringVar(value="—")

        self.btn_prev = ttk.Button(bar2, text="◀ Previous", command=self._prev_page, state="disabled", style="Secondary.TButton")
        self.btn_prev.pack(side="left")

        self.btn_next = ttk.Button(bar2, text="Next ▶", command=self._next_page, state="disabled", style="Secondary.TButton")
        self.btn_next.pack(side="right")

        print(f"{self.theme_manager.get_color('Secondary.TButton')}")

        ttk.Label(bar2, textvariable=self.page_info, style="Subtitle.TLabel").pack(side="left", padx=12)

        self.table = DataFrameTable(self, self.theme_manager)
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
            if self.on_data_loaded:
                self.on_data_loaded(self.df, meta)
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

    def _update_canvas_color(self, canvas):
        if self.theme_manager:
            canvas.configure(bg=self.theme_manager.get_color("bg"))

    def _on_theme_changed(self):
        self._update_canvas_color(self.canvas)