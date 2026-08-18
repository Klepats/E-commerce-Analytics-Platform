from src.data.schema import TransactionRecord


def test_transaction_record_normalizes_numeric_identifiers() -> None:
    transaction = TransactionRecord(
        invoice=489434.0,
        stock_code=85048.0,
        description="15CM CHRISTMAS GLASS BALL 20 LIGHTS",
        quantity=12,
        invoice_date="2009-12-01T07:45:00",
        price=6.95,
        customer_id=13085.0,
        country="United Kingdom",
    )

    assert transaction.invoice == "489434"
    assert transaction.stock_code == "85048"
    assert transaction.customer_id == "13085"
