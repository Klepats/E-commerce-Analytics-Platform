from pathlib import Path

import pandas as pd
import pytest

from src.data.loader import load_transactions


def test_load_transactions_returns_dataframe(tmp_path: Path) -> None:
    csv_path = tmp_path / "transactions.csv"
    csv_path.write_text(
        "\n".join(
            [
                "Invoice,StockCode,Description,Quantity,InvoiceDate,Price,Customer ID,Country",
                "489434,85048,15CM CHRISTMAS GLASS BALL 20 LIGHTS,12,2009-12-01 07:45:00,6.95,13085,United Kingdom",
            ]
        ),
        encoding="utf-8",
    )

    dataframe = load_transactions(csv_path)

    assert isinstance(dataframe, pd.DataFrame)
    assert len(dataframe) == 1
    assert dataframe.loc[0, "invoice"] == "489434"
    assert dataframe.loc[0, "stock_code"] == "85048"


def test_load_transactions_raises_error_for_missing_required_columns(
    tmp_path: Path,
) -> None:
    csv_path = tmp_path / "transactions.csv"
    csv_path.write_text(
        "\n".join(
            [
                "Invoice,StockCode,InvoiceDate",
                "489434,85048,2009-12-01 07:45:00",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        load_transactions(csv_path)
