from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.services.api_client import backend_client

router = Router()


def format_deleted(items: list[dict]) -> str:
    if not items:
        return "Нет удалённых сообщений"
    lines = []
    for item in items:
        text = item.get("text") or "[медиа]"
        chat = item.get("chat_title") or item.get("chat_id")
        deleted_at = item.get("deleted_at")
        lines.append(f"Чат: {chat}\nТекст: {text}\nУдалено: {deleted_at}\n---")
    return "\n".join(lines)


def format_edits(items: list[dict]) -> str:
    if not items:
        return "Нет правок"
    lines = []
    for item in items:
        chat = item.get("chat_title") or item.get("chat_id")
        edited_at = item.get("edited_at")
        lines.append(
            f"Чат: {chat}\nБыло: {item.get('old_text')}\nСтало: {item.get('new_text')}\nВремя: {edited_at}\n---"
        )
    return "\n".join(lines)


@router.message(Command("last_deleted"))
async def last_deleted(message: Message) -> None:
    if message.from_user is None:
        return
    data = await backend_client.get_last_deleted(user_id=message.from_user.id)
    await message.answer(format_deleted(data))


@router.message(Command("last_edited"))
async def last_edited(message: Message) -> None:
    if message.from_user is None:
        return
    data = await backend_client.get_last_edited(user_id=message.from_user.id)
    await message.answer(format_edits(data))
