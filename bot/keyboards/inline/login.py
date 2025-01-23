from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def button():
    return InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text = "Kirish", callback_data = "login"),
                InlineKeyboardButton(text = "Ro'yhatdan o'tish", callback_data = "register")
            ]
        ]
    )