from __future__ import annotations

import asyncio
import logging
from userbot.client_manager import ClientManager
from userbot.config import settings
from userbot.handlers import bind_handlers

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    if not settings.session_string:
        logging.error("[userbot] USERBOT_SESSION_STRING is not set. Exiting without starting Telethon client.")
        return

    manager = ClientManager(
        api_id=settings.api_id,
        api_hash=settings.api_hash,
        session_string=settings.session_string,
        backend_api_url=str(settings.backend_api_url),
    )
    client = await manager.start()
    await bind_handlers(client)
    logging.info("Userbot started")
    await manager.run_forever()

if __name__ == "__main__":
    asyncio.run(main())
