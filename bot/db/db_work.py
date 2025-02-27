"""Работа с базой данных."""

import aiosqlite

DB_PATH = "users.db"


async def init_db():
    """Инициализация базы данных."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT,
                full_name TEXT,
                is_admin INTEGER DEFAULT 0
            )
        """)
        await db.commit()


async def register_user(user_id: int, username: str, full_name: str):
    """
    Регистрация пользователя.

    :user_id: айди пользователя
    :username: никнейм
    :full_name: полное имя
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR IGNORE INTO users (user_id, username, full_name)
            VALUES (?, ?, ?)
        """, (user_id, username, full_name))
        await db.commit()


async def is_registered(user_id: int) -> bool:
    """
    Проверка, зарегистрирован ли пользователь.

    :user_id: айди пользователя.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id FROM users WHERE user_id = ?",
            (user_id,)
        ) as cursor:
            return await cursor.fetchone() is not None


async def get_user(user_id: int):
    """
    Получение данных пользователя.

    :user_id: айди пользователя.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        ) as cursor:
            return await cursor.fetchone()


async def get_users() -> list:
    """Получить список пользователей."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT user_id, username, full_name FROM users"
        )
        users = await cursor.fetchall()
        await cursor.close()
    return users


async def make_admin(user_id: int):
    """
    Назначение пользователя администратором.

    :user_id: айди пользователя.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET is_admin = 1 WHERE user_id = ?",
            (user_id,)
        )
        await db.commit()


async def is_admin(user_id: int) -> bool:
    """
    Проверка, является ли пользователь админом.

    :user_id: айди пользователя.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT is_admin FROM users WHERE user_id = ?",
            (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row and row[0] == 1
