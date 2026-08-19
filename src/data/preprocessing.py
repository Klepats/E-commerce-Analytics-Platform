from dataclasses import dataclass

import pandas as pd


REQUIRED_COLUMNS = (
    "invoice_no",
    "stock_code",
    "quantity",
    "invoice_date",
    "unit_price",
    "country",
)


@dataclass(frozen=True)
class PreprocessingReport:
    """Counts describing the transformations applied to transactions."""

    input_rows: int
    output_rows: int
    removed_duplicates: int
    removed_invalid_rows: int
    removed_zero_quantity_rows: int



def preprocess_transactions(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, PreprocessingReport]:
    """Clean normalized transactions and add fields used by analytics."""

    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(dataframe.columns))
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Missing required columns: {missing}")

    input_rows = len(dataframe)
    cleaned = dataframe.copy()

    cleaned["invoice_no"] = cleaned["invoice_no"].astype("string").str.strip()
    cleaned["stock_code"] = cleaned["stock_code"].astype("string").str.strip()
    cleaned["country"] = cleaned["country"].astype("string").str.strip()
    cleaned["description"] = cleaned["description"].astype("string").str.strip()
    cleaned["customer_id"] = cleaned["customer_id"].astype("string").str.strip()

    cleaned["quantity"] = pd.to_numeric(cleaned["quantity"], errors="coerce")
    cleaned["unit_price"] = pd.to_numeric(cleaned["unit_price"], errors="coerce")
    cleaned["invoice_date"] = pd.to_datetime(cleaned["invoice_date"], errors="coerce")

    valid_rows = (
        cleaned["invoice_no"].notna()
        & cleaned["invoice_no"].ne("")
        & cleaned["stock_code"].notna()
        & cleaned["stock_code"].ne("")
        & cleaned["quantity"].notna()
        & cleaned["invoice_date"].notna()
        & cleaned["unit_price"].notna()
        & cleaned["unit_price"].ge(0)
        & cleaned["country"].notna()
        & cleaned["country"].ne("")
    )
    removed_invalid_rows = int((~valid_rows).sum())
    cleaned = cleaned.loc[valid_rows].copy()

    zero_quantity = cleaned["quantity"].eq(0)
    removed_zero_quantity_rows = int(zero_quantity.sum())
    cleaned = cleaned.loc[~zero_quantity].copy()

    before_deduplication = len(cleaned)
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)
    removed_duplicates = before_deduplication - len(cleaned)

    cleaned["quantity"] = cleaned["quantity"].astype("int64")
    cleaned["revenue"] = cleaned["quantity"] * cleaned["unit_price"]
    cleaned["is_return"] = cleaned["quantity"] < 0
    cleaned["description"] = cleaned["description"].fillna("Unknown product")
    cleaned["customer_id"] = cleaned["customer_id"].replace("", pd.NA)

    report = PreprocessingReport(
        input_rows=input_rows,
        output_rows=len(cleaned),
        removed_duplicates=removed_duplicates,
        removed_invalid_rows=removed_invalid_rows,
        removed_zero_quantity_rows=removed_zero_quantity_rows,
    )
    return cleaned, report
