from fastapi import FastAPI
from routers import product_router
from models import product
from dependencies.database import engine
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from utils.logger import logger

# Создаем все таблицы
product.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API для мониторинга цен на товары",
    version="1.0.0"
)

logger.info("App starting")

app.add_middleware(
    CORSMiddleware,
    # НЕБЕЗОПАСНО !
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Подключаем маршруты
app.include_router(product_router.router, prefix="/products", tags=["Products"])
