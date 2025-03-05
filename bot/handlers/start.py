"""Хэндлеры (обработчики)."""
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from config_reader import config

from utils.check_funcs import contains_bad_words

from db.db_work import (
    register_user, is_registered, is_registered_for_send_msg
)

from kbs.all_kbs import main_kb

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
    username = message.from_user.username or "None"
    full_name = message.from_user.full_name or "None"

    if await is_registered(user_id):
        await message.answer(
            f"Рад тебя видеть снова, <b>{full_name}</b>! 👋\n\n"
            "Я <b>Осирис</b>, твой виртуальный ассистент в мире "
            "технологий.\n\n"
            "Готов помочь тебе узнать больше о моем создателе. Я собрал "
            "самую актуальную информацию и готов с тобой поделиться.\n\n"
            "Просто <i>выбери пункт</i> из меню, чтобы начать работу!",
            reply_markup=main_kb(
                user_telegram_id=message.from_user.id
            )
        )
    else:
        await register_user(user_id, username, full_name)
        await message.answer(
            f"Добро пожаловать, {username}! 👋\n\n"
            "Меня зовут Осирис, и ты только что стал частью моего"
            "маленького технологичного мира. Я создан для того, чтобы "
            "помочь тебе узнать больше о моем создателе и всех проектах "
            "которыми мы занимаемся.\n\n"
            "Все, что тебе нужно - это <i>выбрать пункт</i> в меню, и я "
            "проведу тебя по всем возможностям! Но для начала "
            "давай познакомимся.\n\n Заходи в профиль и расскажи о себе!",
            reply_markup=main_kb(
                user_telegram_id=message.from_user.id
            )
        )


@start_router.callback_query(F.data == "contact")
async def contact_button(callback: CallbackQuery):
    """
    Обработчик сallback_query "contact".

    Вызывает сообщение для редиректа.

    :callback: вызов (class CallbackQuery).
    """
    await callback.message.edit_text(
        "<b>Связь с разработчиком</b>\n\n"
        "Для <b>возможности</b> дальнейшей коммуникации "
        "используйте корректный формат обращения:\n\n"
        "<b>Пример:</b> #связь <i>Привет, я юзер!...</i>\n\n"
        "Напишите ваше сообщение и я передам его!"
    )
    await callback.answer()


@start_router.message(F.text.startswith("#связь "))
async def send_user_message_to_admin(message: Message, bot: Bot):
    """Редирект сообщений пользователей администратору."""
    user_id = message.from_user.id

    if not await is_registered_for_send_msg(user_id):
        await message.answer(
            "⛔ Чтобы отправить сообщение пройдите аутентификацию!\n\n"
            "Перейдите в профиль и заполните следующую информацию:\n"
            "- Имя;\n- Фамилия;\n- E-mail <i>(для связи)</i>."
        )
        return

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
        "В ближайшее время мой создатель обязательно его прочитает."
        )
