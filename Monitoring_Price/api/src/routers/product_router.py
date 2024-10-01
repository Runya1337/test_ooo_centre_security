from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from schemas.product_schema import ProductOut, PriceHistoryOut
from services.product_service import ProductService
from dependencies.database import get_db
import logging

logger = logging.getLogger("uvicorn")
router = APIRouter()

# Добавление товара
@router.post("/", response_model=ProductOut)
def add_product(url: str, service: ProductService = Depends()):
    logger.info("Обрабатывается запрос на добавление элемента с URL: %s", url)
    return service.add_product(url)

# Удаление товара
@router.delete("/{product_id}", response_model=ProductOut)
def delete_product(product_id: int, service: ProductService = Depends()):
    logger.info("Обрабатывается запрос на удаление элемента с ID: %d", product_id)
    return service.delete_product(product_id)

# Получение всех товаров
@router.get("/", response_model=List[ProductOut])
def list_products(service: ProductService = Depends()):
    logger.info("Обрабатывается запрос на получение всех товаров")
    return service.get_all_products()

# Получение истории изменения цен товара
@router.get("/{product_id}/history", response_model=List[PriceHistoryOut])
def get_price_history(product_id: int, service: ProductService = Depends()):
    logger.info("Обрабатывается запрос на историю товара с ID: %d", product_id)
    return service.get_price_history(product_id)

# Обновление цены товара и добавление записи в историю цен
@router.put("/products/{product_id}/update_price/")
def update_product_price(product_id: int, new_price: float, service: ProductService = Depends()):
    logger.info("Обновление цены товара с ID: %d на новую цену: %.2f", product_id, new_price)
    return service.update_price(product_id, new_price)
