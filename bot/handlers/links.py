from aiogram import Router, F
from aiogram.types import CallbackQuery

from kbs.inline_kbs import links_ikb

links_router = Router()


@links_router.callback_query(F.data == "links")
async def send_pages(callback: CallbackQuery):
    """
    Обработчик сallback_query "links".

    Вызывает inline-меню с ссылками на
    социальные сети.

    :callback: вызов (class CallbackQuery).
    """
    await callback.message.edit_text(
        "<b>Ссылки</b>\n\n"
        "Перечень полезных ресурсов и страниц в "
        "социальных сетях.",
        reply_markup=links_ikb()
    )
    await callback.answer()
