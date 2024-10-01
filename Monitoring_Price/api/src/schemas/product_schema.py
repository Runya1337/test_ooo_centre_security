from pydantic import BaseModel, HttpUrl, ConfigDict, Field
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    url: str
    name: Optional[str] = Field(default="Default Name")
    description: Optional[str] = Field(default="Default Description")
    rating: Optional[float] = Field(default=0.0)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    price: Optional[float] = Field(default=0.0)

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class PriceHistoryOut(BaseModel):
    id: int
    product_id: int
    price: float
    timestamp: str

    model_config = ConfigDict(from_attributes=True)
