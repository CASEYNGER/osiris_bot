from aiogram import Router, F
from aiogram.types import Message


settings_router = Router()


@settings_router.message(F.text == "⚙️ Настройки")
async def get_settings(message: Message):
    """
    Обработчик текста "⚙️ Настройки".

    Вызывает меню настроек.

    :message: сообщение (class Message).
    """
    await message.answer(
        "<b>Настройки</b>\n\n"
        "Это раздел с общими настройками виртуального помощника, "
        "где вы можете <i>(в разработке...)</i> ..."
    )
