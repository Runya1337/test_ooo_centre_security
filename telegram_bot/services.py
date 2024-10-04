import requests
from dotenv import load_dotenv
import os
from config import settings


class ProductService:
    def __init__(self, api_url=settings.API_URL):
        self.api_url = api_url

    def add_product(self, url: str):
        return requests.post(
            f"{self.api_url}/products/?url={requests.utils.quote(url)}"
        )

    def search_products(self, query: str):
        return requests.get(f"{self.api_url}/products/search", params={"name": query})

    def get_price_history(self, product_id: int):
        return requests.get(f"{self.api_url}/products/{product_id}/history")
