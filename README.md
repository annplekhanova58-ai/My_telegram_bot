# Telegram Bot — Портфолио

Современный Telegram-бот для сбора заявок с многошаговой формой, валидацией данных и удобным интерфейсом.

![Главное меню](screenshots/menu.png)

## 🚀 Демо-бот

**Живой бот:** [@Randusnam_bot]([https://t.me/твой_ник_бота](https://t.me/Randusnam_bot))

Можешь прямо сейчас протестировать функционал.

## Возможности

- ✅ Интерактивное меню с Inline-кнопками
- ✅ Многошаговая FSM-анкета (Имя → Телефон → Комментарий)
- ✅ Умная валидация российского номера телефона
- ✅ Сохранение всех заявок в SQLite базу данных
- ✅ Мгновенные уведомления администратору
- ✅ Чистая модульная архитектура

## Технологии

- **Python 3.11+**
- **aiogram 3.x**
- **SQLAlchemy** + **aiosqlite**
- **FSM** (Finite State Machine)
- **phonenumbers**
- **python-dotenv**

## Структура проекта

```bash
├── bot.py
├── config.py
├── database.py
├── requirements.txt
├── .env.example
├── data/
│   └── texts.py
├── handlers/
│   └── form.py
├── keyboards/
├── services/
├── states/
└── screenshots/
    ├── menu.png
    ├── message.png
    ├── admin_notification.png
    └── error.png
