from aiogram import Router, Dispatcher

from bot.misc import dp
from bot.utils.helpful_functions import router
from bot.routers import (users, groups, admins, commands)


async def include_routers():
    return (
        router(dispatcher = dp, router = users),
        router(dispatcher = dp, router = groups),
        router(dispatcher = dp, router = admins),
        router(dispatcher = dp, router = commands),

    )