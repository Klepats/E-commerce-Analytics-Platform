import pandas as pd

from src.analytics.sales import calculate_monthly_sales, calculate_sales_metrics


def test_calculate_sales_metrics_separates_returns() -> None:
    dataframe = pd.DataFrame(
        {
            "quantity": [2, 1, -1],
            "unit_price": [10.0, 5.0, 5.0],
        }
    )

    metrics = calculate_sales_metrics(dataframe)

    assert metrics["gross_revenue"] == 25.0
    assert metrics["return_value"] == -5.0
    assert metrics["net_revenue"] == 20.0
    assert metrics["sales_lines"] == 2
    assert metrics["return_lines"] == 1


def test_calculate_monthly_sales_aggregates_orders() -> None:
    dataframe = pd.DataFrame(
        {
            "invoice_no": ["1", "1", "2", "3"],
            "invoice_date": [
                "2011-01-01",
                "2011-01-01",
                "2011-01-15",
                "2011-02-01",
            ],
            "quantity": [2, 1, 4, 1],
            "unit_price": [10.0, 5.0, 2.5, 8.0],
            "customer_id": ["10", "10", "11", "12"],
        }
    )

    monthly = calculate_monthly_sales(dataframe)

    assert list(monthly["month"]) == ["2011-01", "2011-02"]
    assert list(monthly["revenue"]) == [35.0, 8.0]
    assert list(monthly["orders"]) == [2, 1]
    assert list(monthly["customers"]) == [2, 1]
    assert list(monthly["aov"]) == [17.5, 8.0]
