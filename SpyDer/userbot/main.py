from __future__ import annotations

import asyncio
import logging

from userbot.client_manager import manager
from userbot.handlers import bind_handlers

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    client = await manager.start()
    await bind_handlers(client)
    logging.info("Userbot started")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
