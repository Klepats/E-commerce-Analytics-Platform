import pandas as pd
import pytest

from src.data.preprocessing import preprocess_transactions


@pytest.fixture
def transactions() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "invoice_no": ["100", "100", "101", "102", None, "103", "104"],
            "stock_code": ["A", "A", "B", "C", "D", "E", "F"],
            "description": [" Product ", " Product ", None, "Zero", "Invalid", "Return", "Bad"],
            "quantity": [2, 2, 1, 0, 3, -1, 1],
            "invoice_date": [
                "2011-01-01",
                "2011-01-01",
                "2011-01-02",
                "2011-01-03",
                "2011-01-04",
                "2011-01-05",
                "not-a-date",
            ],
            "unit_price": [10.0, 10.0, 5.0, 1.0, 2.0, 4.0, 3.0],
            "customer_id": ["1", "1", "2", "3", "4", None, "5"],
            "country": [" UK ", " UK ", "DE", "FR", "ES", "UK", "IT"],
        }
    )


def test_preprocess_transactions_adds_analytics_fields(transactions: pd.DataFrame) -> None:
    cleaned, report = preprocess_transactions(transactions)

    assert len(cleaned) == 3
    assert list(cleaned["revenue"]) == [20.0, 5.0, -4.0]
    assert list(cleaned["is_return"]) == [False, False, True]
    assert cleaned.loc[1, "description"] == "Unknown product"
    assert cleaned.loc[0, "country"] == "UK"
    assert report.input_rows == 7
    assert report.output_rows == 3
    assert report.removed_duplicates == 1
    assert report.removed_invalid_rows == 2
    assert report.removed_zero_quantity_rows == 1


def test_preprocess_transactions_requires_normalized_columns() -> None:
    with pytest.raises(ValueError, match="Missing required columns: country"):
        preprocess_transactions(pd.DataFrame({"invoice_no": ["100"]}))
