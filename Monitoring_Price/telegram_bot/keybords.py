from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_price_history_button(product_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            "Показать историю цен", callback_data=f"history:{product_id}"
        )
    )
    return markup
