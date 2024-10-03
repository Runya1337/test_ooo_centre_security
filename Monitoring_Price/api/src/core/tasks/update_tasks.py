import asyncio
from celery import shared_task
from services.product_service import ProductService
from dependencies.database import get_db
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

BATCH_SIZE = 50


@shared_task
def update_all_product_prices():
    db_generator = get_db()
    db: Session = next(db_generator)

    product_service = ProductService(db)

    try:
        products = product_service.get_all_products()

        asyncio.run(process_products_in_batches(product_service, products))

    except Exception as e:
        logger.error(f"Ошибка при получении списка продуктов: {str(e)}")
    finally:
        db_generator.close()


async def process_products_in_batches(product_service, products):
    for i in range(0, len(products), BATCH_SIZE):
        batch = products[i : i + BATCH_SIZE]
        logger.info(f"Отправляем батч продуктов с {i+1} по {i+len(batch)} на обработку")

        await run_update_tasks(product_service, batch)

        logger.info(f"Батч с {i+1} по {i+len(batch)} успешно обновлен")


async def run_update_tasks(product_service, products):
    tasks = []

    for product in products:
        tasks.append(product_service.update_price(product.id))

    await asyncio.gather(*tasks)
