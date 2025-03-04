"""Основное приложение для запуска бота."""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault

from db.db_work import init_db

from config_reader import config
from handlers.start import start_router
from handlers.admin import admin_router
from handlers.portfolio import portfolio_router
from handlers.profile import profile_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
logger = logging.getLogger(__name__)

bot = Bot(
    token=config.bot_token.get_secret_value(),
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher(storage=MemoryStorage())


async def set_commands():
    """Настройка командного меню."""
    commands = [
        BotCommand(command="start", description="Запуск бота"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    """Запуск бота."""
    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.include_router(portfolio_router)
    dp.include_router(profile_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await init_db()
    await set_commands()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
