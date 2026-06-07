# My Telegram Bot

Демонстрационный Telegram-бот для сбора заявок с многошаговой формой и валидацией данных.

## Возможности

- Красивое интерактивное меню с Inline-кнопками
- Многошаговая FSM-анкета (Имя → Телефон → Комментарий)
- Валидация российского номера телефона
- Сохранение заявок в SQLite базу данных
- Уведомление администратора о новой заявке
- Чистая модульная архитектура на **aiogram 3.x**

## Технологии

- **Python 3.11+**
- **aiogram 3.7+** (асинхронный)
- SQLAlchemy + aiosqlite
- FSM (Finite State Machine)
- python-dotenv
- phonenumbers (валидация телефона)

## Структура проекта

```bash
├── bot.py
├── config.py
├── database.py
├── requirements.txt
├── .env.example
├── .gitignore
├── data/
│   └── texts.py
├── handlers/
│   └── form.py
├── keyboards/
│   └── __init__.py
├── services/
├── states/
│   └── form.py
└── screenshots/          # (добавь после создания скриншотов)
    ├── menu.png
    └── form.png
