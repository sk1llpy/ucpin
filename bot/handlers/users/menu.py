from aiogram import types, F, html
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session

from bot.decorators import create_session
from bot.keyboards.inline import menu
from bot.misc import bot
from bot.routers import users
from bot.states.register import RegisterState
from db import repository as repo


@users.callback_query(F.data == 'menu__account')
@create_session
async def menu_account_handler(call: types.CallbackQuery, session: Session):
    account = await repo.UsersTableRepository().get_user_account(user_id=call.from_user.id, session=session)
    
    await call.message.edit_text(
        text = f"""{html.bold("Sizning hisobingiz haqida ma'lumot 💰")}
        
📞 Telefon-raqam: {account.phone_number}
📧 Elektron-pochta: {account.email}
💶 Balans (USD): {account.balance_usd}$
💷 Balans (UZS): {account.balance_uzs} so'm""",
        reply_markup = await menu.back()
    )


@users.callback_query(F.data == 'menu__insturction')
async def menu_instruction_handler(call: types.CallbackQuery):
    await call.message.edit_text(
        text = html.bold("Botdan foydalanish uchun qo'llanma 👇") + "\n\n" + "https://t.me/shaxboz_gg",
        reply_markup = await menu.back()
    )


@users.callback_query(F.data == 'menu__contact')
async def menu_contact_handler(call: types.CallbackQuery):
    await call.message.edit_text(
        text = html.bold("""=☎️ Shikoyat va takliflar uchun: @shoxamng
🧑‍💻 Dasturchi: @unrsk1ll"""),
        reply_markup = await menu.back()
    )


# Back to menu
@users.callback_query(F.data == 'back__to_menu')
async def back_to_menu_handler(call: types.CallbackQuery):
    await call.message.edit_text(
        text = html.bold("Kerakli bo'limni tanlang 👇"),
        reply_markup = await menu.button()
    )