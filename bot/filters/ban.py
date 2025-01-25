from aiogram.filters import Filter
from aiogram.enums import ChatType
from aiogram.types import Chat

from sqlalchemy.orm import Session
from db import repository as repo
from bot.decorators import create_session

class IsBanned(Filter):
    def __init__(self, is_banned: bool = True, *args, **kwargs):
        self.is_banned = is_banned

    @create_session
    async def __call__(self, event: object, session: Session, *args, **kwargs) -> bool:
        user_id = event.dict()['from']['user']
        account = await repo.UsersTableRepository().get_user_account(user_id=user_id, session=session)

        return account.is_banned == self.is_banned