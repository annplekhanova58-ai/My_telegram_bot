from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)

from data.texts import ABOUT_TEXT, SERVICES_TEXT, WORKS_TEXT, REVIEWS_TEXT
from config import ADMIN_ID
from database import save_application
from states.form import Form

import phonenumbers
from phonenumbers import NumberParseException

router = Router()


# =========================
# UI КНОПКИ
# =========================

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

back_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ]
)

cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Отмена")]],
    resize_keyboard=True
)


# =========================
# START (APP STYLE)
# =========================

@router.message(CommandStart())
async def start(message: types.Message):

    await message.answer(
        "Привет 👋\n\nВыберите раздел:",
        reply_markup=menu_kb
    )


# =========================
# МЕНЮ (ВСЕ ЧЕРЕЗ edit_text)
# =========================

@router.callback_query(F.data == "about")
async def about(callback: types.CallbackQuery):

    await callback.message.edit_text(ABOUT_TEXT, reply_markup=back_kb)
    await callback.answer()


@router.callback_query(F.data == "services")
async def services(callback: types.CallbackQuery):

    await callback.message.edit_text(SERVICES_TEXT, reply_markup=back_kb)
    await callback.answer()


@router.callback_query(F.data == "works")
async def works(callback: types.CallbackQuery):

    await callback.message.edit_text(WORKS_TEXT, reply_markup=back_kb)
    await callback.answer()


@router.callback_query(F.data == "reviews")
async def reviews(callback: types.CallbackQuery):

    await callback.message.edit_text(REVIEWS_TEXT, reply_markup=back_kb)
    await callback.answer()


# =========================
# BACK (ЕДИНСТВЕННЫЙ)
# =========================

@router.callback_query(F.data == "back")
async def back(callback: types.CallbackQuery):

    await callback.message.edit_text(
        "Привет 👋\n\nВыберите раздел:",
        reply_markup=menu_kb
    )

    await callback.answer()


# =========================
# ЗАЯВКА FSM
# =========================

@router.callback_query(F.data == "order")
async def start_order(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state(Form.name)

    await callback.message.answer(
        "📩 Введите ваше имя:",
        reply_markup=cancel_kb
    )

    await callback.answer()


# =========================
# ИМЯ
# =========================

@router.message(Form.name)
async def get_name(message: types.Message, state: FSMContext):

    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("🚫 Отмена", reply_markup=ReplyKeyboardRemove())
        await message.answer("Выберите раздел:", reply_markup=menu_kb)
        return

    await state.update_data(name=message.text)

    await message.answer("📞 Введите телефон:")
    await state.set_state(Form.phone)


# =========================
# ТЕЛЕФОН
# =========================

@router.message(Form.phone)
async def get_phone(message: types.Message, state: FSMContext):

    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("🚫 Отмена", reply_markup=ReplyKeyboardRemove())
        await message.answer("Выберите раздел:", reply_markup=menu_kb)
        return

    try:
        parsed = phonenumbers.parse(message.text, "RU")

        if not phonenumbers.is_valid_number(parsed):
            await message.answer("❌ Неверный номер")
            return

        phone = phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.E164
        )

    except NumberParseException:
        await message.answer("❌ Ошибка формата")
        return

    await state.update_data(phone=phone)

    await message.answer("💬 Комментарий:")
    await state.set_state(Form.comment)


# =========================
# КОММЕНТАРИЙ
# =========================

@router.message(Form.comment)
async def get_comment(message: types.Message, state: FSMContext):

    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("🚫 Отмена", reply_markup=ReplyKeyboardRemove())
        await message.answer("Выберите раздел:", reply_markup=menu_kb)
        return

    data = await state.update_data(comment=message.text)

    await save_application(
        data["name"],
        data["phone"],
        data["comment"]
    )

    await message.answer("✅ Заявка отправлена!")

    await message.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "📩 НОВАЯ ЗАЯВКА\n\n"
            f"👤 {data['name']}\n"
            f"📞 {data['phone']}\n"
            f"💬 {data['comment']}"
        )
    )

    await state.clear()