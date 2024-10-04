from pydantic import BaseModel

class PriceHistoryOut(BaseModel):
    id: int
    product_id: int
    price: float
    timestamp: str

    class Config:
        from_attributes = True
