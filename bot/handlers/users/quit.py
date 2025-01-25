from aiogram import types, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session

from bot.decorators import create_session
from bot.keyboards.inline import login
from bot.states.register import RegisterState
from bot.routers import users
from db import repository as repo


@users.message(Command("quit"))
@create_session
async def quit_handler(message: types.Message, state: FSMContext, session: Session):
    user = await repo.UsersTableRepository().get_user(user_id=message.from_user.id, session=session)

    if user.is_logined:
        await state.set_state(RegisterState.action)
        repo.UsersTableRepository().edit(
            conditions = {"user_id": message.from_user.id},
            edits = {"is_logined": False, "account_id": None},
            session = session
        )

        await message.answer(
            text = f"""{html.bold("Akkauntdan muvvafaqiyatli chiqildi ✅")}

{html.italic("Kerakli bo'limni tanlang  👇")}""",
            reply_markup = await login.button()
        )
    else:
        await state.set_state(RegisterState.action)
        await message.answer(
            text = f"""{html.bold("Siz akkauntga kirmagansiz ❌")}

{html.italic("Kerakli bo'limni tanlang  👇")}""",
            reply_markup = await login.button()
        )