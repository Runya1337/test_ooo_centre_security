# app/schemas/price_history_schema.py

from pydantic import BaseModel
from typing import Optional

class PriceHistoryOut(BaseModel):
    id: int
    product_id: int
    price: float
    timestamp: str

    class Config:
        from_attributes = True
