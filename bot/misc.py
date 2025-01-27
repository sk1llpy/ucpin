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
        "tolov1 (usd)": {
            "card_number": "karta1 (usd)",
            "cardholder_name": "john smith",
            "phone_number": "+998 77-777-77-77"
        },
        "tolov2 (usd)": {
            "card_number": "karta2 (usd)",
            "cardholder_name": "john smith",
            "phone_number": "+998 88-888-88-88"
        },
        "tolov3 (usd)": {
            "card_number": "karta3 (usd)",
            "cardholder_name": "john smith",
            "phone_number": "+998 99-999-99-99"
        }
    },
    "uzs": {
        "tolov1 (uzs)": {
            "card_number": "karta1 (uzs)",
            "cardholder_name": "john smith"
        },
        "tolov2 (uzs)": {
            "card_number": "karta2 (uzs)"
        },
        "tolov3 (uzs)": {
            "card_number": "karta3 (uzs)",
            "cardholder_name": "john smith",
            "phone_number": "+998 33-333-33-33"
        }
    },
    "min_amount": {
        "usd": 5,
        "uzs": 10000
    }
}