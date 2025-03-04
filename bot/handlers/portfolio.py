from aiogram import Router, F
from aiogram.types import CallbackQuery

from kbs.inline_kbs import portfolio_ikb

portfolio_router = Router()


@portfolio_router.callback_query(F.data == "portfolio")
async def post_portfolio(callback: CallbackQuery):
    """
    Обработчик сallback_query "portfolio".

    Вызывает страницу с портфолио.

    :callback: вызов (class CallbackQuery).
    """
    await callback.message.edit_text(
        "<b>Портфолио</b>\n\n"
        "<i>(В разработке...)</i>",
        reply_markup=portfolio_ikb()
    )
