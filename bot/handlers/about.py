from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from constants.about_me import (
    TEXT_ABOUT_ME, SOFT_SKILLS_LIST, HARD_SKILLS_LIST
)

from kbs.inline_kbs import (
    about_ikb, main_ikb, soft_skills, hard_skills
)

about_router = Router()


@about_router.message(F.text == "О разработчике")
async def post_info(message: Message):
    """
    Обработчик текста "О разработчике".

    Вызывает информацию о разработчике и inline_menu.

    :message: сообщение (class Message).
    """
    await message.answer(
        TEXT_ABOUT_ME,
        reply_markup=about_ikb()
    )


@about_router.callback_query(F.data == "about")
async def get_about_info(callback: CallbackQuery):
    """
    Обработчик сallback_query "about".

    Вызывает страницу с информацией о разработчике.

    :callback: вызов (class CallbackQuery).
    """
    await callback.message.edit_text(
        TEXT_ABOUT_ME,
        reply_markup=about_ikb()
    )
    await callback.answer()


@about_router.callback_query(F.data == "start")
async def go_home_handler(callback: CallbackQuery):
    """
    Обработчик сallback_query "start".

    Вызывает основное inline-меню.

    :callback: вызов (class CallbackQuery).
    """
    await callback.message.edit_text(
        "<b>Главное меню</b>",
        reply_markup=main_ikb()
    )
    await callback.answer()


@about_router.callback_query(F.data == "soft_skills")
async def get_soft_skills(callback: CallbackQuery):
    """
    Обработчик сallback_query "soft_skills".

    Вызывает страницу с информацией о софт-скиллах.

    :callback: вызов (class CallbackQuery).
    """
    await callback.message.edit_text(
        SOFT_SKILLS_LIST,
        reply_markup=soft_skills()
    )
    await callback.answer()


@about_router.callback_query(F.data == "hard_skills")
async def get_hard_skills(callback: CallbackQuery):
    """
    Обработчик сallback_query "hard_skills".

    Вызывает страницу с информацией о хард-скиллах.

    :callback: вызов (class CallbackQuery).
    """
    await callback.message.edit_text(
        HARD_SKILLS_LIST,
        reply_markup=hard_skills()
    )
    await callback.answer()
