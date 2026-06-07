import aiosqlite

DB_PATH = "applications.db"


async def init_db():
    """Инициализация базы данных"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()
        print("✅ База данных инициализирована")


async def save_application(name: str, phone: str, comment: str) -> bool:
    """Сохранение заявки в базу"""
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                """
                INSERT INTO applications (name, phone, comment)
                VALUES (?, ?, ?)
                """,
                (name, phone, comment)
            )
            await db.commit()
            return True
    except Exception as e:
        print(f"❌ Ошибка при сохранении в БД: {e}")
        return False