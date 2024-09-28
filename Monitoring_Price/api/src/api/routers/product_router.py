from fastapi import APIRouter, Depends, HTTPException
from typing import List

from api.schemas.product_schema import ProductCreate, ProductOut, PriceHistoryOut
from api.services.product_service import ProductService
from api.dependencies.database import get_db

router = APIRouter()

@router.post("/", response_model=ProductOut)
def add_product(product: ProductCreate, service: ProductService = Depends()):
    return service.add_product(product)

@router.delete("/{product_id}", response_model=ProductOut)
def delete_product(product_id: int, service: ProductService = Depends()):
    return service.delete_product(product_id)

@router.get("/", response_model=List[ProductOut])
def list_products(service: ProductService = Depends()):
    return service.get_all_products()

@router.get("/{product_id}/history", response_model=List[PriceHistoryOut])
def get_price_history(product_id: int, service: ProductService = Depends()):
    return service.get_price_history(product_id)
