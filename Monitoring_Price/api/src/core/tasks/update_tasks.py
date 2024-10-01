from celery import shared_task
from services.product_service import ProductService
from dependencies.database import get_db
from sqlalchemy.orm import Session


@shared_task
def update_all_product_prices():
    db_generator = get_db()  # Получение генератора сессии
    db: Session = next(db_generator)  # Извлечение сессии из генератора

    product_service = ProductService(db)

    products = product_service.get_all_products()
    for product in products:
        product_service.update_price(product.id)

    # Закрываем сессию после использования
    db_generator.close()
