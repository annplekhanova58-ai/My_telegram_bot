from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ]
)