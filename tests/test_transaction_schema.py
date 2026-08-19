import pytest
from pydantic import ValidationError

from src.data.schema import TransactionRecord


def test_transaction_record_normalizes_numeric_identifiers() -> None:
    transaction = TransactionRecord(
        invoice_no=489434.0,
        stock_code=85048.0,
        description="15CM CHRISTMAS GLASS BALL 20 LIGHTS",
        quantity=12,
        invoice_date="2009-12-01T07:45:00",
        unit_price=6.95,
        customer_id=13085.0,
        country="United Kingdom",
    )

    assert transaction.invoice_no == "489434"
    assert transaction.stock_code == "85048"
    assert transaction.customer_id == "13085"


def test_transaction_record_allows_negative_quantity_for_returns() -> None:
    transaction = TransactionRecord(
        invoice_no="C489434",
        stock_code="85048",
        quantity=-1,
        invoice_date="2009-12-01T07:45:00",
        unit_price=6.95,
        country="United Kingdom",
    )

    assert transaction.quantity == -1


@pytest.mark.parametrize(
    "overrides",
    [
        {"invoice_no": ""},
        {"stock_code": ""},
        {"unit_price": -1.0},
        {"country": ""},
        {"invoice_date": "not-a-date"},
    ],
)
def test_transaction_record_rejects_invalid_values(overrides: dict) -> None:
    valid_record = {
        "invoice_no": "489434",
        "stock_code": "85048",
        "quantity": 12,
        "invoice_date": "2009-12-01T07:45:00",
        "unit_price": 6.95,
        "country": "United Kingdom",
    }
    valid_record.update(overrides)

    with pytest.raises(ValidationError):
        TransactionRecord(**valid_record)
