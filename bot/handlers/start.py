"""Хэндлеры (обработчики)."""
from aiogram import Router, F, Bot
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from constants.cnst_info import (
    WELCOME_AUTH, WELCOME_NON_AUTH, CONTACT_WITH_ADMIN,
)

from config_reader import config

from utils.check_funcs import contains_bad_words

from db.db_work import (
    register_user, is_registered
)

from kbs.all_kbs import request_contact_kb
from kbs.inline_kbs import about

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Обработчик команды /start.

    Автоматически добавляет пользователя в БД
    и отправляет приветственное сообщение в зависимости
    от статуса пользователя.

    :message: сообщение (class Message).
    """
    user_id = message.from_user.id

    if await is_registered(user_id):
        await message.answer(
            WELCOME_NON_AUTH,
            reply_markup=about()
        )
    else:
        await message.answer(
            WELCOME_AUTH,
            reply_markup=request_contact_kb(
                user_telegram_id=message.from_user.id
            )
        )


@start_router.message(F.content_type == ContentType.CONTACT)
async def get_contact(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "None"
    full_name = message.from_user.full_name or "None"
    phone_number = message.contact.phone_number
    if message.contact.user_id == user_id:
        await register_user(user_id, username, full_name, phone_number)
        await message.answer(
            f"✅ Спасибо! Ваш номер {phone_number} сохранен.\n\n"
            "Нажмите на кнопку ниже:",
            reply_markup=about()
        )
    else:
        await message.answer(
            "Пожалуйста, отправьте свой номер через кнопку ниже. 📲",
            reply_markup=request_contact_kb
        )


@start_router.callback_query(F.data == "contact")
async def contact_button(callback: CallbackQuery):
    """
    Обработчик сallback_query "contact".

    Вызывает сообщение для редиректа.

    :callback: вызов (class CallbackQuery).
    """
    await callback.message.edit_text(
        CONTACT_WITH_ADMIN,
        reply_markup=about()
    )
    await callback.answer()


@start_router.message(F.text.startswith("#связь "))
async def send_user_message_to_admin(message: Message, bot: Bot):
    """Редирект сообщений пользователей администратору."""
    text = message.text.replace("#связь ", "").strip()

    if not text:
        await message.answer(
            "Пожалуйста, соблюдайте <b>формат</b> обращения!\n\n"
            "<b>Пример:</b> #связь <i>Привет, я юзер!...</i>\n\n"
        )
        return

    if contains_bad_words(text):
        await message.answer(
            "❌ <b>Сообщение не отправлено.</b>\n\n"
            "Ваше сообщение содержит запрещенные слова и может "
            "быть оскорбительным и унижающим достоинство других "
            "людей."
            )
        return

    admin_id = config.admin
    await bot.send_message(
        admin_id,
        f"📩 <b>Сообщение от @{message.from_user.username}:</b>\n\n{text}"
    )
    await message.answer(
        "✅ <b>Сообщение успешно отправлено.</b>\n\n"
        "В ближайшее время мой создатель обязательно его прочитает.",
        reply_markup=about()
        )
