from aiogram import Dispatcher

from bot.filters.chat_type import Chat
from bot.filters.content_type import ContentType
from bot.filters.text import Text

from bot.middlewares.ban import CheckBanMiddleware


async def setup_middlewares(dispatcher: Dispatcher):
    CheckBanMiddleware.register(dispatcher)

async def setup_filters(dispatcher: Dispatcher):
    dispatcher.message.filter(Chat)
    dispatcher.message.filter(Text)
    dispatcher.message.filter(ContentType)
