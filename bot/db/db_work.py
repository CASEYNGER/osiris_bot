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
                name TEXT,
                surname TEXT,
                email TEXT,
                phone_number INT,
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


async def is_registered(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT user_id FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            return result is not None


async def is_registered_for_send_msg(user_id: int) -> bool:
    """
    Проверка, зарегистрирован ли пользователь.

    :user_id: айди пользователя.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT name, surname, email FROM users WHERE user_id = ?",
            (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            if result:
                name, surname, email = result
            return bool(name and surname and email)
        return False


async def get_user(user_id: int):
    """
    Получение данных пользователя.

    :user_id: айди пользователя.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT name, surname, email, phone_number FROM users WHERE user_id = ?",
            (user_id,)
        ) as cursor:
            return await cursor.fetchone()


async def get_users() -> list:
    """Получить список пользователей."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT user_id, username, name, surname FROM users"
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


async def update_name(user_id: int, new_name: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET name = ? WHERE user_id = ?",
            (new_name, user_id)
        )
        await db.commit()


async def update_surname(user_id: int, new_surname: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET surname = ? WHERE user_id = ?",
            (new_surname, user_id)
        )
        await db.commit()


async def update_phone_number(user_id: int, new_number: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET phone_number = ? WHERE user_id = ?",
            (new_number, user_id)
        )
        await db.commit()


async def update_email(user_id: int, new_email: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET email = ? WHERE user_id = ?",
            (new_email, user_id)
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
