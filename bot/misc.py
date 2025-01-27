from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode

from data.config import BotSettings


bot_settings = BotSettings()
storage = MemoryStorage()
dp = Dispatcher(
    storage = storage
)
bot = Bot(
    token = bot_settings.token,
    default = DefaultBotProperties(
        parse_mode = ParseMode.HTML
    )
)
payment_data = {
    "usd": {
        "binance": {
            "card_number": "karta1 (usd)",
            "cardholder_name": "john smith",
            "phone_number": "+998 77-777-77-77"
        },
        "trc": {
            "card_number": "karta2 (usd)",
            "cardholder_name": "john smith",
            "phone_number": "+998 88-888-88-88"
        },
        "bep": {
            "card_number": "karta3 (usd)",
            "cardholder_name": "john smith",
            "phone_number": "+998 99-999-99-99"
        },
        "bybit": {
            "card_number": "karta3 (usd)",
            "cardholder_name": "john smith",
            "phone_number": "+998 20-000-00-00"
        }
    },
    "uzs": {
        "uzcard": {
            "card_number": "karta1 (uzs)",
            "cardholder_name": "john smith"
        },
        "humo": {
            "card_number": "karta2 (uzs)"
        }
    },
    "min_amount": {
        "usd": 5,
        "uzs": 10000
    }
}
payment_names = {
    "usd": {
        "binance": "Binance Pay",
        "trc": "TRC20",
        "bep": "BEP20",
        "bybit": "Bybit"
    },
    "uzs": {
        "uzcard": "UzCard",
        "humo": "HUMO Card"
    }
}