from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Create your buttons here.
async def button():
    return InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(
                    text="🛒 UC Harid qilish", callback_data='menu__purchase')
            ],
            [
                InlineKeyboardButton(
                    text="👤 Kabinet", callback_data='menu__account'),
                InlineKeyboardButton(
                    text="🌐 Buyurtmalar tarixi", callback_data='menu__purchases_history')
            ],
            [
                InlineKeyboardButton(
                    text="💰 Xisob to'ldirish", callback_data='menu__top_up')
            ],
            [
                InlineKeyboardButton(
                    text="📕 Qo'llanma", callback_data='menu__insturction'),
                InlineKeyboardButton(
                    text="☎️ Yordam uchun", callback_data='menu__contact')
            ]
        ]
    )
    

async def back():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅️ Orqaga", callback_data='back__to_menu')
            ]
        ]
    )

