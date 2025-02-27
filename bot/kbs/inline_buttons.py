"""Inline-кнопки."""

from aiogram.types import InlineKeyboardButton

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

# Кнопка "Портфолио"
PORTFOLIO = InlineKeyboardButton(
                    text="Портфолио",
                    callback_data="portfolio"
                )

# Кнопка "Ссылки"
LINKS = InlineKeyboardButton(
                    text="Ссылки",
                    callback_data="pages"
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
