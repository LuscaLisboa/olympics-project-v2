from __future__ import annotations

import os

import pandas as pd


def load_table(file_path: str, sample_rows: int | None = None) -> tuple[pd.DataFrame, dict]:
    """Load .xlsx, .xls or .csv into a DataFrame.
    - If sample_rows is not None, returns only head(sample_rows).
    Returns(df, meta)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    if ext in (".xlsx", ".xls"):
        df = pd.read_excel(file_path)
    elif ext == ".csv":
        try:
            df = pd.read_csv(file_path)
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding="latin-1")
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    if sample_rows is not None:
        df = df.head(sample_rows).copy()

    meta = {
        "name": os.path.basename(file_path),
        "rows": len(df),
        "cols": len(df.columns),
        "ext": ext,
        "path": os.path.abspath(file_path),
    }
    return df, meta