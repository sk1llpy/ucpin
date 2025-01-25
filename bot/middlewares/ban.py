from aiogram import types, html
from aiogram.types import TelegramObject
from aiogram.enums import ChatType
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from typing import Any, Awaitable, Callable, Dict
from sqlalchemy.orm import Session

from bot.decorators import create_session
from bot.misc import bot
from db import repository as repo


class CheckBanAndChatMiddleware(BaseMiddleware):
    @create_session
    async def __call__(
        self, 
        handler: Callable[
            [TelegramObject, Dict[str, Any]], Awaitable[Any]
        ],
        event: TelegramObject, 
        data: Dict[str, Any], 
        session: Session
    ) -> Any:
        event_data = event.dict()

        if event_data['chat']['type'] == ChatType.PRIVATE:
            account = await repo.UsersTableRepository().get_user_account(
                user_id = event_data['from_user']['id'], 
                session = session
            )

            if ((not account.is_banned) if account else True) and (not event_data.get('text', None) == "/quit"):
                return await handler(event, data)
            else:
                await bot.send_message(
                    chat_id = event_data['chat']['id'], 
                    text = html.bold("Sizning xisobingiz administrator tomonidan ban qilingan! 🚫"), 
                    reply_to_message_id = event_data['message_id']
                )