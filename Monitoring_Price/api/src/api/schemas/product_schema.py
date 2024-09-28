from pydantic import BaseModel, HttpUrl
from typing import Optional

class ProductBase(BaseModel):
    url: HttpUrl
    name: str
    description: Optional[str] = None
    rating: Optional[float] = None

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True

class PriceHistoryOut(BaseModel):
    id: int
    product_id: int
    price: float
    timestamp: str

    class Config:
        orm_mode = True
