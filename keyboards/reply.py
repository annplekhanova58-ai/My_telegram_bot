from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📌 Обо мне", callback_data="about"),
            InlineKeyboardButton(text="💼 Услуги", callback_data="services")
        ],
        [
            InlineKeyboardButton(text="🛠 Работы", callback_data="works"),
            InlineKeyboardButton(text="⭐ Отзывы", callback_data="reviews")
        ],
        [
            InlineKeyboardButton(text="📩 Оставить заявку", callback_data="order")
        ]
    ]
)