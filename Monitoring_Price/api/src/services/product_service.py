from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

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
    def parse_product_price(cls, url):
        if "mvideo" in url:
            parser = MVideoParser()
        elif "ozon" in url:
            parser = OzonParser()
        elif "avito" in url:
            parser = AvitoParser()
        else:
            raise HTTPException(status_code=400, detail="Неизвестный источник")
        return parser.parse(url)

    def add_product(self, url: str) -> ProductOut:
        # Используем метод parse_product_price для получения данных
        parsed_data = self.parse_product_price(url)

        # Создаем объект ProductCreate с данными из парсера
        product_create = ProductCreate(
            url=url,
            name=parsed_data.get("title", "Default Name"),
            description=parsed_data.get("description", "Default Description"),
            rating=parsed_data.get("rating", 0),
            price=parsed_data.get("price", 0.0)
        )

        # Проверка на существование продукта с таким URL
        existing_product = self.repository.get_by_url(product_create.url)
        if existing_product:
            raise HTTPException(status_code=400, detail="Product already exists")

        # Создание продукта в базе данных
        product = self.repository.create(product_create)
        return ProductOut.from_orm(product)

    def update_price(self, product_id: int) -> ProductOut:
        # Получаем продукт через репозиторий
        product = self.repository.get_by_id(product_id)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Обновляем цену продукта
        parsed_data = self.parse_product_price(product.url)
        new_price = parsed_data.get("price")

        # Обновляем поле 'price' в объекте 'product'
        product.price = new_price

        # Создаем новую запись в PriceHistory
        price_history_entry = PriceHistory(
            product_id=product.id,
            price=new_price,
            timestamp=datetime.utcnow().isoformat()
        )

        # Добавляем запись в историю и сохраняем изменения
        self.db.add(price_history_entry)
        self.db.commit()

        # Обновляем объект 'product' после сохранения в базе данных
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
