from bot.misc import bot
from bot.decorators import create_session
from bot.routers import users
from bot.keyboards.inline import menu, login
from bot.states.register import RegisterState

from aiogram import types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import Session
from db import repository as repo


@users.message(CommandStart())
@create_session
async def command_start(message: types.Message, state: FSMContext, session: Session):
    user = await repo.UsersTableRepository().get_user(
        user_id=message.from_user.id, session=session
    )

    if user:
        if user.is_logined:
            await message.answer(
                text = f"""<b>Salom {message.from_user.first_name} 👋</b>

<i>Kerakli bo'limni tanlang 👇</i>""",
                reply_markup = await menu.button()
            )
        else:
            await state.set_state(RegisterState.action)
            
            await message.answer(
                text = """<b>Kerakli bo'limni tanlang 👇</b>""",
                reply_markup = await login.button()
            )
    else:
        await state.set_state(RegisterState.action)
        
        await repo.UsersTableRepository().create_user(
            user=message.from_user, is_logined=False, session=session)
        
        await message.answer(
            text = """<b>Kerakli bo'limni tanlang 👇</b>""",
            reply_markup = await login.button()
        )
