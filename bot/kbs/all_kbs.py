"""Обычные клавиатуры для меню."""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def request_contact_kb(user_telegram_id: int):
    """
    Добавляет верификацию по номеру телефона.

    :user_telegram_id: идентификационный номер пользователя.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📞 Отправить номер",
                    request_contact=True
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
