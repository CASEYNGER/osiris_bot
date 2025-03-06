from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from constants.templates import NOT_ADMIN

from db.db_work import (
    get_users, is_admin, make_admin
)

from kbs.inline_kbs import about

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
        await message.answer(NOT_ADMIN, reply_markup=about())
        return
    if not users:
        await message.answer("База данных пуста.", reply_markup=about())
        return
    text = "\n".join(
        [f"- {user[0]}, @{user[1]}, {user[2]};" for user in users]
    )
    await message.answer(
        f"<b>Список пользователей:</b>\n\n{text}",
        reply_markup=about()
        )


@admin_router.message(Command("make_admin"))
async def make_admin_command(message: Message):
    """
    Обработчик команды /make_admin.

    Делает пользователя администратором (только для админов).

    :message: сообщение (class Message).
    """
    if not await is_admin(message.from_user.id):
        await message.answer(NOT_ADMIN, reply_markup=about())
        return

    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        await message.answer("⚠ Использование: /make_admin <user_id>")
        return

    user_id = int(args[1])
    await make_admin(user_id)
    await message.answer(
        f"✅ Пользователь {user_id} теперь администратор!",
        reply_markup=about()
        )


@admin_router.message(Command("admin_panel"))
async def admin_panel(message: Message):
    """
    Обработчик команды /admin_panel.

    Панель администратора (доступ только у админов).

    :message: сообщение (class Message).
    """
    if not await is_admin(message.from_user.id):
        await message.answer(NOT_ADMIN, reply_markup=about())
        return

    await message.answer(
        "🔧 <b>Добро пожаловать в панель администратора!</b>\n\n"
        "<b>Доступные команды:</b>\n\n"
        "/get_users - получить список пользователей;\n"
        "/admin_panel - активация админ-панели;\n"
        "/make_admin id - сделать администратором.",
        reply_markup=about()
    )
