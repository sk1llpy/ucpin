from aiogram import Dispatcher

from bot.filters.ban import IsBanned

from bot.middlewares.ban import CheckBanAndChatMiddleware


async def setup_middlewares(dispatcher: Dispatcher):
    dispatcher.message.middleware(CheckBanAndChatMiddleware())

async def setup_filters(dispatcher: Dispatcher):
    dispatcher.message.filter(IsBanned)
