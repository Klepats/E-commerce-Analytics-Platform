import pandas as pd


def calculate_sales_metrics(dataframe: pd.DataFrame) -> dict[str, float | int]:
    """Calculate line-level sales and return metrics."""

    required_columns = {"quantity", "unit_price"}
    missing_columns = sorted(required_columns - set(dataframe.columns))
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Missing required columns: {missing}")

    revenue = dataframe["quantity"] * dataframe["unit_price"]
    is_return = dataframe["quantity"] < 0

    return {
        "gross_revenue": float(revenue.loc[~is_return].sum()),
        "return_value": float(revenue.loc[is_return].sum()),
        "net_revenue": float(revenue.sum()),
        "sales_lines": int((~is_return).sum()),
        "return_lines": int(is_return.sum()),
        "average_line_value": float(revenue.mean()),
    }


def calculate_monthly_sales(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Aggregate positive sales by month with orders, customers, and AOV."""

    required_columns = {"invoice_no", "invoice_date", "quantity", "unit_price"}
    missing_columns = sorted(required_columns - set(dataframe.columns))
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Missing required columns: {missing}")

    sales = dataframe.loc[dataframe["quantity"] > 0].copy()
    sales["revenue"] = sales["quantity"] * sales["unit_price"]
    sales["month"] = pd.to_datetime(sales["invoice_date"]).dt.to_period("M").astype(str)

    group_columns = {
        "revenue": ("revenue", "sum"),
        "orders": ("invoice_no", "nunique"),
    }
    if "customer_id" in sales.columns:
        group_columns["customers"] = ("customer_id", "nunique")

    monthly = sales.groupby("month", as_index=False).agg(**group_columns)
    monthly["aov"] = monthly["revenue"] / monthly["orders"]
    return monthly
