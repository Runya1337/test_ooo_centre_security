import asyncio
from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from utils.parsers.parser import MVideoParser, OzonParser, AvitoParser
from schemas.product_schema import ProductCreate, ProductOut, PriceHistoryOut
from models.product import Product, PriceHistory
from repositories.product_repository import ProductRepository
from dependencies.database import get_db


class ProductService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repository = ProductRepository(db)
        self.db = db

    @classmethod
    #TODO передать в маппинг
    def parse_product_price(cls, url):
        if "mvideo" in url:
            parser = MVideoParser(url)
        elif "ozon" in url:
            parser = OzonParser(url)
        elif "avito" in url:
            parser = AvitoParser(url)
        else:
            # должен выдать другой экзепшен, можно кастомный, а сверху словить hhtp
            raise HTTPException(status_code=400, detail="Неизвестный источник")
        return parser

    async def add_product(self, url: str) -> ProductOut:
        parser = self.parse_product_price(url)
        parsed_data = await parser.parse()
        product_create = ProductCreate(
            url=url,
            name=parsed_data.get("name", "Default Name"),
            description=parsed_data.get("description", "Default Description"),
            rating=parsed_data.get("rating", 0),
            price=parsed_data.get("price", 0.0),
        )

        existing_product = self.repository.get_by_url(product_create.url)
        if existing_product:
            raise HTTPException(status_code=400, detail="Product already exists")

        product = self.repository.create(product_create)
        return ProductOut.from_orm(product)

    async def update_price(self, product_id: int) -> ProductOut:
        product = self.repository.get_by_id(product_id)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        parser = self.parse_product_price(product.url)
        new_price = await parser.get_price()

        product.price = new_price

        price_history_entry = PriceHistory(
            product_id=product.id,
            price=new_price,
            timestamp=datetime.utcnow().isoformat(),
        )

        self.db.add(price_history_entry)
        self.db.commit()

        self.db.refresh(product)

        return ProductOut.from_orm(product)

    def make_fake_history(self, product_id: int) -> ProductOut:
        product = self.db.query(Product).filter_by(id=product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        end_date = datetime.now() - timedelta(days=1)  # Вчера
        start_date = end_date - timedelta(days=730)  # Два года назад
        total_days = (end_date - start_date).days + 1  # Количество дней

        current_price = product.price or 100.0

        price_history_entries = []

        for day in range(total_days):
            date = start_date + timedelta(days=day)
            price_change = random.uniform(-5, 5)
            current_price += current_price * (price_change / 100)
            current_price = max(current_price, 1.0)

            price_history_entry = PriceHistory(
                product_id=product.id, price=round(current_price, 2), timestamp=date
            )
            price_history_entries.append(price_history_entry)

        self.db.bulk_save_objects(price_history_entries)
        self.db.commit()

        self.db.refresh(product)

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

    def search_products(self, name: str) -> List[Product]:
        return self.repository.search_by_name(name)
