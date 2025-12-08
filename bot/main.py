from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import settings
from bot.handlers import common, start
from bot.services.api_client import backend_client

logging.basicConfig(level=logging.INFO)


def build_dp() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(start.router, common.router)
    return dp


async def main() -> None:
    bot = Bot(token=settings.bot_token, parse_mode=ParseMode.HTML)
    dp = build_dp()
    try:
        await dp.start_polling(bot)
    finally:
        await backend_client.close()


if __name__ == "__main__":
    asyncio.run(main())
