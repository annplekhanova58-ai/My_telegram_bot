# Telegram Bot — Портфолио

Демонстрационный Telegram-бот для сбора заявок с многошаговой FSM-формой и валидацией данных.

## Возможности

- Красивое интерактивное меню с Inline-кнопками
- Многошаговая анкета (Имя → Телефон → Комментарий)
- Валидация российского номера телефона
- Сохранение заявок в SQLite базу данных
- Уведомления администратору о новых заявках
- Чистая модульная архитектура (handlers, states, keyboards, services)

## Технологии

- **Python 3.11+**
- **aiogram 3.x** (асинхронный фреймворк)
- SQLAlchemy + aiosqlite
- FSM (Finite State Machine)
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
├── services/
├── states/
│   └── form.py
└── screenshots/
    ├── menu.png
    ├── message.png
    ├── admin_notification.png
    └── error.png
