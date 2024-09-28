from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from api.schemas.product_schema import ProductCreate, ProductOut, PriceHistoryOut
from api.models.product import Product, PriceHistory
from api.repositories.product_repository import ProductRepository
from api.dependencies.database import get_db

class ProductService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repository = ProductRepository(db)

    def add_product(self, product_create: ProductCreate) -> ProductOut:
        existing_product = self.repository.get_by_url(product_create.url)
        if existing_product:
            raise HTTPException(status_code=400, detail="Product already exists")
        product = self.repository.create(product_create)
        return ProductOut.from_orm(product)

    def delete_product(self, product_id: int) -> ProductOut:
        product = self.repository.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        self.repository.delete(product)
        return ProductOut.from_orm(product)

    def get_all_products(self) -> List[ProductOut]:
        products = self.repository.get_all()
        return [ProductOut.from_orm(p) for p in products]

    def get_price_history(self, product_id: int) -> List[PriceHistoryOut]:
        history = self.repository.get_price_history(product_id)
        return [PriceHistoryOut.from_orm(h) for h in history]
