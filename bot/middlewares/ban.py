from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from sqlalchemy.orm import Session

from bot.decorators import create_session
from db import repository as repo


class CheckBanMiddleware(BaseMiddleware):
    @create_session
    async def __call__(self, handler, event, data, session: Session):
        print("\n\n\n\n")
        print(data)
        print("\n\n\n\n")
        print(event)
        print("\n\n\n\n")
        # account = await repo.UsersTableRepository().get_user_account()
        

        return await super().__call__(handler, event, data)