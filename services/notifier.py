from config import ADMIN_ID

async def notify_admin(bot, data):
    text = (
        f"📩 Новая заявка\n\n"
        f"👤 {data['name']}\n"
        f"📞 {data['phone']}\n"
        f"💬 {data['comment']}"
    )

    await bot.send_message(ADMIN_ID, text)