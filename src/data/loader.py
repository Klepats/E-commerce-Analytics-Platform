from pathlib import Path
from typing import Iterable

import pandas as pd

from src.data.schema import RAW_COLUMN_MAPPING, REQUIRED_TRANSACTION_COLUMNS


SOURCE_TEXT_COLUMNS = {
    "Invoice": "string",
    "StockCode": "string",
    "Customer ID": "string",
}


def read_csv(file_path: str | Path) -> pd.DataFrame:
    """Read a CSV file into a pandas DataFrame."""

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    return pd.read_csv(path, dtype=SOURCE_TEXT_COLUMNS)


def read_excel(file_path: str | Path) -> pd.DataFrame:
    """Read an Excel file into a pandas DataFrame."""

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Excel file not found: {path}")

    return pd.read_excel(path, dtype=SOURCE_TEXT_COLUMNS)


def ensure_columns(dataframe: pd.DataFrame, required_columns: Iterable[str]) -> None:
    missing_columns = sorted(set(required_columns) - set(dataframe.columns))
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Missing required columns: {missing}")


def normalize_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Convert Online Retail II source column names to project column names."""

    return dataframe.rename(columns=RAW_COLUMN_MAPPING)


def load_transactions(file_path: str | Path) -> pd.DataFrame:
    """Load raw Online Retail II transactions and check required columns."""

    path = Path(file_path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        dataframe = read_excel(path)
    else:
        dataframe = read_csv(path)

    dataframe = normalize_columns(dataframe)
    ensure_columns(dataframe, REQUIRED_TRANSACTION_COLUMNS)
    return dataframe
