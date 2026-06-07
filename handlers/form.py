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

from data.texts import ABOUT_TEXT, SERVICES_TEXT, WORKS_TEXT, REVIEWS_TEXT, CONSENT_TEXT
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

consent_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Согласен", callback_data="consent_yes")],
        [InlineKeyboardButton(text="❌ Отказаться", callback_data="consent_no")]
    ]
)


# =========================
# START
# =========================

@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Привет 👋\n\nВыберите раздел:",
        reply_markup=menu_kb
    )


# =========================
# МЕНЮ
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


@router.callback_query(F.data == "back")
async def back(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Привет 👋\n\nВыберите раздел:",
        reply_markup=menu_kb
    )
    await callback.answer()


# =========================
# FSM ЗАЯВКА — СОГЛАСИЕ СРАЗУ
# =========================

@router.callback_query(F.data == "order")
async def start_order(callback: types.CallbackQuery, state: FSMContext):
    # Показываем согласие на обработку ПД ПЕРЕД началом формы
    await callback.message.answer(
        CONSENT_TEXT,
        parse_mode="HTML",
        reply_markup=consent_kb
    )
    await callback.answer()


@router.callback_query(F.data == "consent_yes")
async def process_consent_yes(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.name)
    await callback.message.edit_text(
        "✅ Спасибо! Согласие получено.\n\n📝 Теперь введите ваше имя:",
        reply_markup=None
    )
    # Добавляем cancel клавиатуру для следующего шага
    await callback.message.answer("Введите ваше имя:", reply_markup=cancel_kb)


@router.callback_query(F.data == "consent_no")
async def process_consent_no(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "❌ Согласие на обработку персональных данных не дано.\nЗаявка отменена."
    )
    await state.clear()


# =========================
# Остальные шаги формы
# =========================

@router.message(Form.name)
async def get_name(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await cancel_form(message, state)
        return

    await state.update_data(name=message.text.strip())
    await message.answer("📞 Теперь введите номер телефона (в любом формате):")
    await state.set_state(Form.phone)


@router.message(Form.phone)
async def get_phone(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await cancel_form(message, state)
        return

    try:
        parsed = phonenumbers.parse(message.text, "RU")
        if not phonenumbers.is_valid_number(parsed):
            await message.answer("❌ Неверный номер телефона. Попробуйте ещё раз:")
            return

        phone = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except NumberParseException:
        await message.answer("❌ Не удалось распознать номер. Попробуйте в формате +7XXXXXXXXXX:")
        return

    await state.update_data(phone=phone)
    await message.answer("💬 Расскажите подробнее о вашей задаче (комментарий):")
    await state.set_state(Form.comment)


@router.message(Form.comment)
async def get_comment(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await cancel_form(message, state)
        return

    await state.update_data(comment=message.text.strip())

    data = await state.get_data()

    success = await save_application(
        data["name"], data["phone"], data["comment"]
    )

    if success:
        await message.answer(
            "✅ Заявка успешно отправлена!\nЯ свяжусь с вами в ближайшее время.",
            reply_markup=ReplyKeyboardRemove()
        )

        # Уведомление админу
        await message.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 <b>НОВАЯ ЗАЯВКА</b>\n\n"
                 f"👤 Имя: {data['name']}\n"
                 f"📞 Телефон: {data['phone']}\n"
                 f"💬 Комментарий: {data['comment']}\n"
                 f"✅ Согласие на обработку ПД: Да",
            parse_mode="HTML"
        )
    else:
        await message.answer("❌ Произошла ошибка при сохранении заявки.")

    await state.clear()


async def cancel_form(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🚫 Заявка отменена", reply_markup=ReplyKeyboardRemove())
    await message.answer("Выберите раздел:", reply_markup=menu_kb)