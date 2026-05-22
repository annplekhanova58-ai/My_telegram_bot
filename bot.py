import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database import init_db
from handlers.form import router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(router)


async def main():
    print("BOT STARTED")

    await init_db()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())