"""Inline-клавиатуры."""

from aiogram.types import InlineKeyboardMarkup

from .inline_buttons import (
    ABOUT_DEV, GO_HOME, GO_BACK, PORTFOLIO,
    LINKS, CONTACT, SOFT_SKILLS, HARD_SKILLS,
    GITHUB, LINKED_IN, TG_CHANNEL, INSTAGRAM,
    EDIT_PROFILE_NAME, EDIT_PROFILE_EMAIL,
    EDIT_PROFILE_NUMBER, EDIT_PROFILE_SURNAME,
    MY_PROFILE, OSIRIS, BACK_TO_PORTFOLIO, OSIRIS_GIT_HUB,
    BACK_TO_PROFILE
    )


def back_to_profile_ikb():
    """
    Вернуться в профиль.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[[BACK_TO_PROFILE]]
    )


def edit_profile_ikb():
    """
    Редактировать профиль.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [EDIT_PROFILE_NAME],
            [EDIT_PROFILE_SURNAME],
            [EDIT_PROFILE_EMAIL],
            [EDIT_PROFILE_NUMBER],
            [GO_HOME]
        ]
    )


def main_ikb():
    """
    Главная страница.

    Создает основное inline-меню.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [ABOUT_DEV],
            [PORTFOLIO, LINKS],
            [CONTACT],
            [MY_PROFILE]
        ]
    )


def about():
    """
    Страница с информацией о ABOUT_DEV.

    Кнопка возвращает на главную страницу.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[[GO_HOME]]
    )


def about_ikb():
    """
    Страница с информацией о разработчике.

    Создает inline-меню при нажатии
    "О разработчике" или при вызове callback_query
    "about".
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [SOFT_SKILLS, HARD_SKILLS],
            [GO_HOME]
        ]
    )


def links_ikb():
    """
    Страница с ссылками.

    Вызывает inline-меню при вызове
    callback_query "about".
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [TG_CHANNEL, INSTAGRAM],
            [GITHUB, LINKED_IN],
            [GO_HOME]
        ]
    )


def portfolio_ikb():
    """
    Страница с информацией о PORTFOLIO.

    Кнопка возвращает на главную страницу.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [OSIRIS],
            [GO_HOME]
        ]
    )


def osiris_ikb():
    """
    Страница с информаией о боте OSIRIS.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [OSIRIS_GIT_HUB],
            [BACK_TO_PORTFOLIO]
        ]
    )


def soft_skills():
    """
    Страница с информацией о SOFT_SKILLS.

    Кнопка возвращает на предыдущую страницу.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[[GO_BACK]]
    )


def hard_skills():
    """
    Страница с информацией о HARD_SKILLS.

    Кнопка возвращает на предыдущую страницу.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[[GO_BACK]]
    )
