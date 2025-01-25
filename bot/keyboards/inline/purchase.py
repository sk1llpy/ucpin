from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.orm import Session

from db import repository as repo


async def balance_type():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💰 Redeem-code ($)", callback_data='purchase__USD'),
                InlineKeyboardButton(text="💰 Redeem-code (so'm)", callback_data='purchase__UZS')
            ],
            [
                InlineKeyboardButton(text="⬅️ Orqaga", callback_data='back__to_menu')
            ]
        ]
    )

async def packages(balance_type: str, session: Session):
    uc_packages = await repo.UCPackagesTableRepository().get_all_ucpackages(session)

    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=f"""{package.title} ({(str(package.price_uzs) + " so'm") if balance_type == "uzs" else (str(package.price_usd) + "$")})""",
                callback_data=f"purchase__{package.id}"
            )
        ] for package in uc_packages
    ]

    inline_keyboard.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data='purchase__back_balance_type')
    ])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

async def counter(current: int = 1):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="-", callback_data='minus'),
                InlineKeyboardButton(text=f"{current}", callback_data=f"{current}"),
                InlineKeyboardButton(text="+", callback_data='plus')
            ],
            [
                InlineKeyboardButton(text="✅ Tasdiqlash", callback_data='purchase__confirm'),
            ],
            [
                InlineKeyboardButton(text="⬅️ Orqaga", callback_data='purchase__back_to_uc_package')
            ]
        ]
    )


async def confirm():
    return InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text="✅ Ha", callback_data="purchase__yes"),
                InlineKeyboardButton(text="❌ Yo'q", callback_data="purchase__no")
            ],
            [
                InlineKeyboardButton(text="⬅️ Orqaga", callback_data='purchase__back_to_counter')
            ]
        ]
    )