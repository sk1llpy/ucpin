import os

from aiogram import types, F, html
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session

from bot.decorators import create_session
from bot.keyboards.inline import menu
from bot.misc import bot
from bot.routers import users
from bot.states.register import RegisterState
from bot.to_excel import purchase_history_excel
from bot.filters.ban import IsBanned
from db import repository as repo


@users.callback_query(IsBanned(), F.data == 'menu__account')
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


@users.callback_query(IsBanned(), F.data == 'menu__insturction')
async def menu_instruction_handler(call: types.CallbackQuery):
    await call.message.edit_text(
        text = html.bold("Botdan foydalanish uchun qo'llanma 👇") + "\n\n" + "https://t.me/shaxboz_gg",
        reply_markup = await menu.back()
    )


@users.callback_query(IsBanned(), F.data == 'menu__contact')
async def menu_contact_handler(call: types.CallbackQuery):
    await call.message.edit_text(
        text = html.bold("""☎️ Shikoyat va takliflar uchun: @shoxamng"""),
        reply_markup = await menu.back()
    )


@users.callback_query(IsBanned(), F.data == 'menu__purchases_history')
@create_session
async def menu_purchase_history_handler(call: types.CallbackQuery, session: Session):
    account = await repo.UsersTableRepository().get_user_account(user_id=call.from_user.id, session=session)
    purchases = await repo.AccountsTableRepository().get_purchase_history_as_dict(account_id=account.id, session=session)

    if purchases:
        filepath = await purchase_history_excel(data=purchases)

        await call.message.edit_text(
            text = f"""{html.bold("💰 Jami haridlar: ")} {len(purchases)} ta
            
{html.italic("Barcha xaridlar excel formatida yuborilmoqda ⏳")}""",
            reply_markup = await menu.back()
        )

        await call.message.reply_document(document=types.FSInputFile(path=filepath))

        os.remove(path=filepath)
    else:
        await call.message.edit_text(
            text = html.bold("Hech qanday haridlar topilmadi ❌"),
            reply_markup = await menu.back()
        )

# Back to menu
@users.callback_query(IsBanned(), F.data == 'back__to_menu')
async def back_to_menu_handler(call: types.CallbackQuery):
    await call.message.edit_text(
        text = html.bold("Kerakli bo'limni tanlang 👇"),
        reply_markup = await menu.button()
    )


# If user is banned
@users.callback_query(IsBanned(True))
async def if_user_banned_handler(call: types.CallbackQuery):
    await call.message.edit_text(text = html.bold("Sizning xisobingiz administrator tomonidan ban qilingan! 🚫"))