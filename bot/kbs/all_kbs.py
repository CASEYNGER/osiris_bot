"""Обычные клавиатуры для меню."""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_kb(user_telegram_id: int):
    """
    Создает основное меню.

    :user_telegram_id: идентификационный номер пользователя.
    """
    kb = [
        [KeyboardButton(text="О разработчике")],
        [KeyboardButton(text="Профиль")],
        # [KeyboardButton(text="⚙️ Настройки")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите пункт меню:"
    )
    return keyboard
