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
            "card_number": "524055065",
            "cardholder_name": "Shaxboz GG"
        },
        "trc": {
            "card_number": "TBrePv2vXp6LiAKkhU1vRhsj2HFrfM1N8f"
        },
        "bep": {
            "card_number": "0xdb12b1f9090e133f3d14ee046ca9bf96c79efb10"
        }
        # "bybit": {
        #     "card_number": "karta3 (usd)",
        #     "cardholder_name": "john smith"
        # }
    },
    "uzs": {
        "uzcard": {
            "card_number": "5440 8100 0528 0127",
            "cardholder_name": "Abduxalil Babamuradov",
            "phone_number": "+998994033004"
        },
        "humo": {
            "card_number": "9860 1866 0157 1117",
            "cardholder_name": "Abduxalil Babamuradov",
            "phone_number": "+998994033004"
        }
    },
    "min_amount": {
        "usd": 10,
        "uzs": 500000
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