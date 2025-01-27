from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.misc import payment_data

async def balance_type():
    return InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text = "💰 USD Balans", callback_data="topup__USD"),
                InlineKeyboardButton(text = "💰 USD Balans", callback_data="topup__UZS"),
            ],
            [
                InlineKeyboardButton(text="⬅️ Orqaga", callback_data='back__to_menu')
            ]
        ]
    )


async def payment_type(balance_type: str):
    inline_keyboard = [
        [
            InlineKeyboardButton(text = f"💳 {payment}", callback_data = f"topup__{payment}")
        ] for payment in list(payment_data[balance_type].keys())
    ]

    inline_keyboard.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data='topup__back_to_balance_type')
    ])

    return InlineKeyboardMarkup(inline_keyboard = inline_keyboard)


async def confirm_admin(topup_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"topup_confirm__{topup_id}"),
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"topup_deny__{topup_id}")
            ]
        ]
    )