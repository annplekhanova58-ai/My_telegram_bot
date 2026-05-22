import aiosqlite

DB_PATH = "applications.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            comment TEXT
        )
        """)

        await db.commit()


async def save_application(name, phone, comment):

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            INSERT INTO applications (
                name,
                phone,
                comment
            )
            VALUES (?, ?, ?)
            """,
            (name, phone, comment)
        )

        await db.commit()