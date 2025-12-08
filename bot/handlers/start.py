from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.keyboards.menus import MenuFactory
from bot.services.api_client import backend_client

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    user = message.from_user
    if user is None:
        return

    is_premium = user.is_premium
    await backend_client.upsert_user(telegram_id=user.id, is_premium=is_premium)
    kb = MenuFactory.start_menu(is_premium=is_premium).as_markup()
    await message.answer(
        "Выберите режим работы. Бизнес-режим доступен только с Telegram Premium.",
        reply_markup=kb,
    )


@router.callback_query(lambda c: c.data and c.data.startswith("mode:"))
async def mode_callback(call: CallbackQuery) -> None:
    if call.from_user is None or call.data is None:
        return
    mode = call.data.split(":", maxsplit=1)[1]
    if mode == "premium_required":
        await call.answer("Нужен Telegram Premium", show_alert=True)
        return
    await backend_client.mark_mode(user_id=call.from_user.id, mode=mode)
    if mode == "userbot":
        text = (
            "Режим userbot выбран. Позже сюда добавим инструкцию по подключению session string."
        )
    else:
        text = "Режим бизнес выбран. Скоро добавим подключение business сообщений."
    await call.message.answer(text)
    await call.answer()
