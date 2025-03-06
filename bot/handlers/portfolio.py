from aiogram import Router, F
from aiogram.types import CallbackQuery

from kbs.inline_kbs import portfolio_ikb, osiris_ikb

portfolio_router = Router()


@portfolio_router.callback_query(F.data == "portfolio")
async def post_portfolio(callback: CallbackQuery):
    """
    Обработчик сallback_query "portfolio".

    Вызывает страницу с портфолио.

    :callback: вызов (class CallbackQuery).
    """
    await callback.message.edit_text(
        "<b>Портфолио</b>\n\n",
        reply_markup=portfolio_ikb()
    )
    await callback.answer()


@portfolio_router.callback_query(F.data == "get_osiris")
async def post_osiris(callback: CallbackQuery):
    """
    Обработчик callback_query "get_osiris".

    Вызывает страницу с информацией о боте.

    :callback: вызов (class CallbackQuery).
    """
    await callback.message.edit_text(
            "<b>Telegram-бот OSIRIS</b>\n\n"
            "<b>Стэк:</b>\n"
            "🔹 <b>Python 3.12.4 </b>\nЯзык программирования.\n"
            "🔹 <b>Aiogram 3</b>\nРабота с TelegramBotAPI.\n"
            "🔹 <b>Aiosqlite</b>\nРабота с базой данных.\n"
            "🔹 <b>Asyncio</b>\nАсинхронное выполнение задач.\n"
            "🔹 <b>Logging</b>\nВедение логов работы бота и отладки.\n"
            "🔹 <b>Re</b>\nОбработка и валидация текста.",
            reply_markup=osiris_ikb()
    )
    await callback.answer()
