import random
import asyncio
from abc import ABC, abstractmethod
from utils.parsers.product_list import names_products, product_dis


class Parser(ABC):
    def __init__(self, url):
        self.url = url

    async def get_page(self):
        await asyncio.sleep(random.uniform(0.5, 2))  # Имитация задержки сети
        return {
            "price": random.randint(1000, 100000),
            "name": random.choice(names_products),
            "description": random.choice(product_dis),
            "rating": str(random.uniform(1, 5)),
        }

    @abstractmethod
    async def parse(self):
        pass


class BaseParser(Parser):
    async def parse(self):
        page = await self.get_page()
        return {
            "price": await self.get_price(page),
            "name": await self.get_name(page),
            "description": await self.get_description(page),
            "rating": await self.get_rating(page),
        }

    async def get_price(self, page=None):
        if page is None:
            page = (
                await self.get_page()
            )
        return page["price"]

    async def get_name(self, page=None):
        if page is None:
            page = await self.get_page()
        return page["name"]

    async def get_description(self, page=None):
        if page is None:
            page = await self.get_page()
        return page["description"]

    async def get_rating(self, page=None):
        if page is None:
            page = await self.get_page()
        return page["rating"]


class MVideoParser(BaseParser):
    async def get_price(self, page=None):
        return await super().get_price(page)

    async def get_name(self, page=None):
        return await super().get_name(page)

    async def get_description(self, page=None):
        return await super().get_description(page)

    async def get_rating(self, page=None):
        return await super().get_rating(page)


class OzonParser(BaseParser):
    async def get_price(self, page=None):
        return await super().get_price(page)

    async def get_name(self, page=None):
        return await super().get_name(page)

    async def get_description(self, page=None):
        return await super().get_description(page)

    async def get_rating(self, page=None):
        return await super().get_rating(page)


class AvitoParser(BaseParser):
    async def get_price(self, page=None):
        return await super().get_price(page)

    async def get_name(self, page=None):
        return await super().get_name(page)

    async def get_description(self, page=None):
        return await super().get_description(page)

    async def get_rating(self, page=None):
        return await super().get_rating(page)
