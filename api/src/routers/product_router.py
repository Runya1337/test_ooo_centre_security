from fastapi import APIRouter, Depends, HTTPException
from typing import List

from schemas.product_schema import ProductOut, PriceHistoryOut
from services.product_service import ProductService
import logging

logger = logging.getLogger("uvicorn")
router = APIRouter()


@router.post("/", response_model=ProductOut)
async def add_product(url: str, service: ProductService = Depends()):
    return await service.add_product(url)


@router.delete("/{product_id}", response_model=ProductOut)
def delete_product(product_id: int, service: ProductService = Depends()):
    return service.delete_product(product_id)


@router.get("/", response_model=List[ProductOut])
def list_products(service: ProductService = Depends()):
    return service.get_all_products()


@router.get("/{product_id}/history", response_model=List[PriceHistoryOut])
def get_price_history(product_id: int, service: ProductService = Depends()):
    return service.get_price_history(product_id)


@router.put("/products/{product_id}/update_price/")
async def update_product_price(
    product_id: int, new_price: float, service: ProductService = Depends()
):
    return await service.update_price(product_id, new_price)


@router.post("/products/{product_id}/fake_history/")
def add_fake_history(product_id: int, service: ProductService = Depends()):
    return service.make_fake_history(product_id)


@router.get("/search", response_model=List[ProductOut])
def search_products(name: str, service: ProductService = Depends()):
    products = service.search_products(name)
    if not products:
        raise HTTPException(status_code=404, detail="Продукты не найдены")
    return products
