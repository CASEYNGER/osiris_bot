from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from constants.templates import NOT_ADMIN

from db.db_work import (
    get_users, is_admin, make_admin
)

admin_router = Router()


@admin_router.message(Command("get_users"))
async def send_users_list(message: Message):
    """
    Обработчик команды /get_users.

    Отправляет список пользователей (только для админов).

    :message: сообщение (class Message).
    """
    users = await get_users()
    if not await is_admin(message.from_user.id):
        await message.answer(NOT_ADMIN)
        return
    if not users:
        await message.answer("База данных пуста.")
        return
    text = "\n".join(
        [f"- {user[0]}, @{user[1]}, {user[2]} {user[3]};" for user in users]
    )
    await message.answer(f"<b>Список пользователей:</b>\n\n{text}")


@admin_router.message(Command("make_admin"))
async def make_admin_command(message: Message):
    """
    Обработчик команды /make_admin.

    Делает пользователя администратором (только для админов).

    :message: сообщение (class Message).
    """
    if not await is_admin(message.from_user.id):
        await message.answer(NOT_ADMIN)
        return

    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        await message.answer("⚠ Использование: /make_admin <user_id>")
        return

    user_id = int(args[1])
    await make_admin(user_id)
    await message.answer(f"✅ Пользователь {user_id} теперь администратор!")


@admin_router.message(Command("admin_panel"))
async def admin_panel(message: Message):
    """
    Обработчик команды /admin_panel.

    Панель администратора (доступ только у админов).

    :message: сообщение (class Message).
    """
    if not await is_admin(message.from_user.id):
        await message.answer(NOT_ADMIN)
        return

    await message.answer(
        "🔧 <b>Добро пожаловать в панель администратора!</b>\n\n"
        "<b>Доступные команды:</b>\n\n"
        "/status - узнать статус пользователя;\n"
        "/get_users - получить список пользователей;\n"
    )
