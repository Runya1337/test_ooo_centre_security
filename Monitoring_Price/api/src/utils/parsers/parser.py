import random
import time
from abc import ABC, abstractmethod

from utils.parsers.product_list import names_products, product_dis

class Parser(ABC):
    list = []
    @abstractmethod
    def parse(self, url: str):
        pass

# Абстрактный класс, который будет реализовывать общую логику
class BaseParser(Parser):
    def parse(self, url: str):
        # Здесь может быть общая логика
        return self.extract_data(url)

    @abstractmethod
    def extract_data(self, url: str):
        pass

# Парсер для M.Video
class MVideoParser(BaseParser):
    def extract_data(self, url: str):
        # Условно спим, якобы парсим
        time.sleep(random.randint(1, 20)/10)
        return {
            'price': random.randint(100, 100000),
            'title': random.choice(names_products),
            'description': random.choice(product_dis),
            'rating': 5.0,  # Дефолтный рейтинг
        }

# Парсер для Ozon
class OzonParser(BaseParser):
    def extract_data(self, url: str):
        # Возвращаем дефолтные значения
        return {
            'price': 100,
            'title': 'Ozon Product Title',
            'description': 'Ozon Product Description',
            'rating': 4.5,  # Дефолтный рейтинг
        }

# Парсер для Авито
class AvitoParser(BaseParser):
    def extract_data(self, url: str):
        # Возвращаем дефолтные значения
        return {
            'price': 100,
            'title': 'Avito Product Title',
            'description': 'Avito Product Description',
            'rating': 4.0,  # Дефолтный рейтинг
        }
