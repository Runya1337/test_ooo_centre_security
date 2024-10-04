from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Command
from services import ProductService
from chart_generator import PriceChartGenerator

product_service = ProductService()


async def add_link(message: types.Message):
    link = message.get_args()
    if link:
        response = product_service.add_product(link)
        if response.status_code == 200:
            await message.reply("Товар успешно добавлен в мониторинг!")
        elif response.status_code == 400:
            if response.json().get("detail") == "Product already exists":
                await message.reply("Этот товар уже существует в системе мониторинга.")
            else:
                await message.reply(
                    f"Ошибка при добавлении товара: {response.status_code} - {response.text}"
                )
        else:
            await message.reply(
                f"Ошибка при добавлении товара: {response.status_code} - {response.text}"
            )
    else:
        await message.reply("Пожалуйста, укажите ссылку после команды /add.")


async def search_product(message: types.Message):
    query = message.get_args()
    if query:
        response = product_service.search_products(query)
        if response.status_code == 200:
            products = response.json()
            if products:
                for product in products:
                    product_id = product["id"]
                    reply = (
                        f"Название: {product['name']}\n"
                        f"Цена: {product['price']} руб.\n"
                        f"Описание: {product['description']}\n"
                        f"Рейтинг: {product['rating']}\n"
                        f"Ссылка: {product['url']}"
                    )
                    markup = InlineKeyboardMarkup()
                    markup.add(
                        InlineKeyboardButton(
                            "Показать историю цен",
                            callback_data=f"history:{product_id}",
                        )
                    )

                    await message.reply(reply, reply_markup=markup)
            else:
                await message.reply("Товаров по данному запросу не найдено.")
        else:
            await message.reply("Ошибка при поиске товаров.")
    else:
        await message.reply(
            "Пожалуйста, укажите ключевые слова для поиска после команды /search."
        )


async def send_price_history(call: types.CallbackQuery):
    product_id = call.data.split(":")[1]
    response = product_service.get_price_history(product_id)

    if response.status_code == 200:
        history = response.json()
        if history:
            chart_generator = PriceChartGenerator(history)
            year_chart = chart_generator.generate_year_chart()
            month_chart = chart_generator.generate_month_chart()

            await call.message.reply("Отправляю графики изменения цен.")
            await call.message.answer_photo(
                year_chart, caption="График изменения цен за год"
            )
            await call.message.answer_photo(
                month_chart, caption="График изменения цен за месяц"
            )
        else:
            await call.message.reply("История цен для этого товара отсутствует.")
    else:
        await call.message.reply(
            f"Ошибка при получении истории цен: {response.status_code}"
        )


def register_handlers(dp):
    dp.register_message_handler(add_link, commands=["add"])
    dp.register_message_handler(search_product, commands=["search"])
    dp.register_callback_query_handler(
        send_price_history, lambda call: call.data.startswith("history")
    )
