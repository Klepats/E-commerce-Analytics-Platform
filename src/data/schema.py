from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TransactionRecord(BaseModel):
    """Schema for one Online Retail II transaction row."""

    model_config = ConfigDict(str_strip_whitespace=True)

    invoice_no: str = Field(min_length=1)
    stock_code: str = Field(min_length=1)
    description: Optional[str] = None
    quantity: int
    invoice_date: datetime
    unit_price: float = Field(ge=0)
    customer_id: Optional[str] = None
    country: str = Field(min_length=1)

    @field_validator("invoice_no", "stock_code", "customer_id", mode="before")
    @classmethod
    def normalize_identifier(cls, value: object) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)


TRANSACTION_COLUMNS = tuple(TransactionRecord.model_fields.keys())
REQUIRED_TRANSACTION_COLUMNS = (
    "invoice_no",
    "stock_code",
    "quantity",
    "invoice_date",
    "unit_price",
    "customer_id",
)

RAW_COLUMN_MAPPING = {
    "Invoice": "invoice_no",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "Price": "unit_price",
    "Customer ID": "customer_id",
    "Country": "country",
}

RAW_TRANSACTION_COLUMNS = tuple(RAW_COLUMN_MAPPING.keys())

DATASET_URL = (
    "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
)
