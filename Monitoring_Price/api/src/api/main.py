from fastapi import FastAPI
from api.routers import product_router
from api.models import product, price_history
from api.dependencies.database import engine
from api.core.config import settings

# Создаем все таблицы
product.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API для мониторинга цен на товары",
    version="1.0.0"
)

# Подключаем маршруты
app.include_router(product_router.router, prefix="/products", tags=["Products"])
