from aiogram import Bot, Dispatcher, executor
from handlers import register_handlers  # Импорт функции для регистрации обработчиков
from config import settings

bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Регистрация обработчиков
register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
