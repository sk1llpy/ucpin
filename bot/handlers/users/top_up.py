import time

from aiogram import types, F, html
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session

from bot.decorators import create_session
from bot.keyboards.inline import menu
from bot.misc import bot, bot_settings
from bot.routers import users
from bot.states.purchase import PurchaseState
from bot.filters.ban import IsBanned
from db import repository as repo


@users.callback_query(IsBanned(), F.data == "menu__top_up")
@create_session
async def top_up_balance_handler(call: types.CallbackQuery, state: FSMContext, session: Session):                  
    ...
