"""Inline-кнопки."""

from aiogram.types import InlineKeyboardButton

# Кнопка "Telegram-бот OSIRIS"
OSIRIS = InlineKeyboardButton(
                text="Telegram-бот OSIRIS",
                callback_data="get_osiris"
                )

# Кнопка "GitHub"
OSIRIS_GIT_HUB = InlineKeyboardButton(
                text="GitHub",
                url="https://github.com/CASEYNGER/osiris_bot"
                )

# Кнопка "К портфолио"
BACK_TO_PORTFOLIO = InlineKeyboardButton(
                text="<< К портфолио",
                callback_data="portfolio"
                )

# Кнопка "Портфолио"
PORTFOLIO = InlineKeyboardButton(
                    text="Портфолио",
                    callback_data="portfolio"
                )

# Кнопка "Профиль"
MY_PROFILE = InlineKeyboardButton(
                text="Профиль",
                callback_data="go_to_profile"
                )

# Кнопка "<< В профиль"
BACK_TO_PROFILE = InlineKeyboardButton(
                text="<< В профиль",
                callback_data="go_to_profile"
                )


# Кнопка "Редактировать имя"
EDIT_PROFILE_NAME = InlineKeyboardButton(
                text="Изменить имя",
                callback_data="edit_profile_name"
                )

# Кнопка "Редактировать фамилию"
EDIT_PROFILE_SURNAME = InlineKeyboardButton(
                text="Изменить фамилию",
                callback_data="edit_profile_surname"
                )

# Кнопка "Редактировать e-mail"
EDIT_PROFILE_EMAIL = InlineKeyboardButton(
                text="Изменить e-mail",
                callback_data="edit_profile_email"
                )

# Кнопка "Редактировать номер"
EDIT_PROFILE_NUMBER = InlineKeyboardButton(
                text="Изменить номер телефона",
                callback_data="edit_profile_number"
                )

# Кнопка "О разработчике"
ABOUT_DEV = InlineKeyboardButton(
                text="О разработчике",
                callback_data="about"
                )

# Кнопка "На главную"
GO_HOME = InlineKeyboardButton(
                text="<< На главную",
                callback_data="start"
                )

# Кнопка "Назад"
GO_BACK = InlineKeyboardButton(
                text="<< Назад",
                callback_data="about"
                )

# Кнопка "Ссылки"
LINKS = InlineKeyboardButton(
                    text="Ссылки",
                    callback_data="links"
                )

# Кнопка "Связаться"
CONTACT = InlineKeyboardButton(
                    text="Связаться",
                    callback_data="contact"
                )

# Кнопка "Софт-скиллы"
SOFT_SKILLS = InlineKeyboardButton(
                    text="Софт-скиллы",
                    callback_data="soft_skills"
                )

# Кнопка "Хард-скиллы"
HARD_SKILLS = InlineKeyboardButton(
                    text="Хард-скиллы",
                    callback_data="hard_skills"
                )

# Кнопка "LinkedIn"
LINKED_IN = InlineKeyboardButton(
                    text="LinkedIn",
                    url="https://www.linkedin.com/"
                    "in/ivan-kobzev-2307a8353?"
                    "utm_source=share&utm_campaign="
                    "share_via&utm_content=profile&utm_medium=ios_app"
                )

# Кнопка "GitHub"
GITHUB = InlineKeyboardButton(
                    text="GitHub",
                    url="https://github.com/caseynger/"
                )

# Кнопка "Telegram-канал"
TG_CHANNEL = InlineKeyboardButton(
                    text="Telegram-канал",
                    url="https://t.me/caseynger/"
                )

# Кнопка "Instagram"
INSTAGRAM = InlineKeyboardButton(
                    text="Instagram",
                    url="https://instagram.com/caseynger/"
                )
