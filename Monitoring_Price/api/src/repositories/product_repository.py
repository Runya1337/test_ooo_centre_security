from typing import List, Optional
from sqlalchemy.orm import Session

from models.product import Product, PriceHistory
from schemas.product_schema import ProductCreate

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_url(self, url: str) -> Optional[Product]:
        url_str = str(url)
        return self.db.query(Product).filter(Product.url == url_str).first()

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def create(self, product_create: ProductCreate) -> Product:
        product_data = product_create.dict()
        product_data['url'] = str(product_data['url'])  # Преобразуем Url в строку
        product = Product(**product_data)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()

    def get_all(self) -> List[Product]:
        return self.db.query(Product).all()

    def get_price_history(self, product_id: int) -> List[PriceHistory]:
        return self.db.query(PriceHistory).filter(PriceHistory.product_id == product_id).all()
