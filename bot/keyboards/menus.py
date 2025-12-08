from __future__ import annotations

from aiogram.utils.keyboard import InlineKeyboardBuilder


class MenuFactory:
    @staticmethod
    def start_menu(is_premium: bool) -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()
        builder.button(text="Подключить через сессию", callback_data="mode:userbot")
        if is_premium:
            builder.button(text="Подключить бизнес-режим", callback_data="mode:business")
        else:
            builder.button(text="Бизнес-режим (нужен Premium)", callback_data="mode:premium_required")
        builder.adjust(1)
        return builder
