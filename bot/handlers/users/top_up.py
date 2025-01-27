import time

from aiogram import types, F, html
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session

from bot.decorators import create_session
from bot.keyboards.inline import menu, top_up
from bot.misc import bot, bot_settings, payment_data, payment_names
from bot.routers import users
from bot.states.top_up import TopUpState
from bot.filters.ban import IsBanned
from db import repository as repo


@users.callback_query(IsBanned(), F.data == "menu__top_up")
@create_session
async def top_up_handler(call: types.CallbackQuery, state: FSMContext, session: Session):                  
    await state.set_state(TopUpState.balance_type)
    await call.message.edit_text(
        text=html.bold("Kerakli balans turini tanlang tanlang 👇"),
        reply_markup=await top_up.balance_type()
    )


@users.callback_query(IsBanned(), F.data.in_(["topup__USD", "topup__UZS", "back__to_menu"]), StateFilter(TopUpState.balance_type))
@create_session
async def top_up_balance_type_handler(call: types.CallbackQuery, state: FSMContext, session: Session):
    if not call.data == "back__to_menu":
        await state.update_data(balance_type = ("usd" if call.data.endswith("USD") else "uzs"))
        await state.set_state(TopUpState.payment_type)
        
        await call.message.edit_text(
            text=html.bold("Kerakli tolov turini tanlang 👇"),
            reply_markup=await top_up.payment_type(call.data.split("__")[1].lower())
        )
    else:
        await call.message.edit_text(
            text = html.bold("Kerakli bo'limni tanlang 👇"),
            reply_markup = await menu.button()
        )

        await state.clear()


@users.callback_query(IsBanned(), lambda call: str(call.data).startswith("topup__"), StateFilter(TopUpState.payment_type))
@create_session
async def top_up_payment_type_handler(call: types.CallbackQuery, state: FSMContext, session: Session):
    if not call.data == "topup__back_to_balance_type":
        data = await state.get_data()
        balance_type = data.get("balance_type")
        payment_type = call.data.split("__")[1]

        if payment_type in list(payment_data[balance_type].keys()):
            card = payment_data[balance_type][payment_type]

            text = f"""{html.bold("💳 Karta (hisob) raqam:  ")} {html.code(card['card_number'])}"""

            if card.get('cardholder_name'):
                text += f"""\n{html.bold("👤 Ism-familya:  ") + card.get('cardholder_name')}"""

            if card.get('phone_number'):
                text += f"""\n{html.bold("📞 Telefon-raqam:  " + card.get('phone_number'))}"""

            await state.update_data(payment_type = payment_type)
            await state.set_state(TopUpState.amount)
            msg = await call.message.edit_text(
                text = f"""{text}

{html.italic("Ushbu kartaga to'lov qilganingizdan so'ng to'lov summasini kiriting!")}
{html.italic("Masalan: " + (f"100000 (orasiga nuqta qoyib yozish mumkin emas, minimal summa: {payment_data['min_amount']['uzs']})" if balance_type == 'uzs' else f'5 yoki 5.20 (nuqta orqali centlarni kiritish mumkin, minimal summa: {payment_data["min_amount"]["usd"]})'))}.""",
                reply_markup = await top_up.back('payment_type')
            )

            await state.update_data(text = msg.text)
    else:
        await state.set_state(TopUpState.balance_type)
        await call.message.edit_text(
            text = html.bold("Kerakli balans turini tanlang tanlang 👇"),
            reply_markup = await top_up.balance_type()
        )


@users.callback_query(IsBanned(), F.data == 'topup__back_to_payment_type', StateFilter(TopUpState.amount))
async def top_up_back_to_payment_type_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    balance_type = data.get('balance_type')

    await state.set_state(TopUpState.payment_type)
    await call.message.edit_text(
        text = html.bold("Kerakli tolov turini tanlang 👇"),
        reply_markup = await top_up.payment_type(balance_type)
    )


@users.message(F.content_type == types.ContentType.TEXT, StateFilter(TopUpState.amount))
async def top_up_amount_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    balance_type = data.get('balance_type')
    amount_str = message.text

    try:
        amount = float(amount_str)

        if amount >= (payment_data['min_amount']['uzs'] if balance_type == 'uzs' else payment_data['min_amount']['usd']):
            await state.update_data(amount = amount)
            await state.set_state(TopUpState.cheque)

            await message.reply(text=html.bold("Ma'lumot qa'bul qilindi ✅"))
            await message.answer(
                text = f"""{html.bold("To'lov chekini yuboring 🧾")}

{html.italic("Telegram-bot chekni faqatgina rasm ko'rinishida qabul qiladi, havola yoki fayl korinishidagi chek qabul qilinmaydi ⚠️")}""",
                reply_markup = await top_up.back("amount")
            )
        else:
            await message.reply(
                text = html.bold("Siz minimal summadan kam miqdor kiritdingiz ❌"),
                reply_markup = await top_up.back('payment_type')
            )
    except:
        await message.answer(
            text = html.bold("Siz noto'g'ri formatda kiritdingiz, iltimos qaytadan kiriting ❌"),
            reply_markup = await top_up.back('payment_type')
        )


@users.callback_query(IsBanned(), F.data == 'topup__back_to_amount', StateFilter(TopUpState.cheque))
async def top_up_back_to_amount_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    balance_type = data.get('balance_type')
    text = data.get('text')

    await state.set_state(TopUpState.amount)
    await call.message.edit_text(
        text = text,
        reply_markup = await top_up.back('payment_type')
    )


@users.message(F.content_type == types.ContentType.PHOTO, StateFilter(TopUpState.cheque))
@create_session
async def top_up_cheque_handler(message: types.Message, state: FSMContext, session: Session):
    photo = message.photo[-1].file_id

    data = await state.get_data()
    balance_type = data.get('balance_type')
    payment_type = data.get('payment_type')
    amount = data.get('amount')

    account = await repo.UsersTableRepository().get_user_account(user_id=message.from_user.id, session=session)
    payment = await repo.TopUpsTableRepository().create_top_up(
        data = {
            "balance_type": balance_type,
            "payment_type": payment_type,
            "amount": amount,
            "account_id": account.id
        },
        session = session
    )

    await bot.send_photo(
        chat_id = bot_settings.admin_group,
        photo = photo,
        caption = f"""{html.bold("#TOP_UP")}

 -- To'lov haqida ma'lumot 👇

{html.italic("💳 To'lov turi: " + str(data.get('balance_type').upper() + " — " + payment_names[balance_type][data.get('payment_type')]))}
{html.italic("💰 To'lov summasi: " + str(data.get('amount')) + ("$" if data.get('balance_type') == "usd" else " so'm"))}

 -- Akkaunt va telegram akkaunt haqida ma'lumot 👇

{html.italic("📞 Telefon-raqam: " + str(account.phone_number))}
{html.italic("📧 Elektron-pochta: " + str(account.email))}
{html.italic("👤 To'liq ismi: " + message.from_user.full_name)}
{html.italic("🆔 Telegram ID: " + str(message.from_user.id))}
{html.italic("👤 Username: " + "@" + str(message.from_user.username))}
""",
        reply_markup = await top_up.confirm_admin(payment.id)
    )

    await message.answer(text=html.bold("To'lov haqidagi ma'lumotlar adminlarga yuborildi! Tez orada balansingizga pul to'ldiriladi ⏳"))
    await message.answer(
        text = html.bold("Kerakli bo'limni tanlang 👇"),
        reply_markup = await menu.button()
    )

    await state.clear()


@users.callback_query(lambda call: call.data.startswith("topup_confirm__") or call.data.startswith("topup_deny__"))
@create_session
async def top_up_admin_handler(call: types.CallbackQuery, session: Session):
    topup_id = int(call.data.split("__")[1])
    topup = await repo.TopUpsTableRepository().get_top_up(topup_id=topup_id, session=session)

    account = await repo.AccountsTableRepository().get_account(account_data={"id": topup.account_id}, session=session)
    user = await repo.UsersTableRepository().get_user_by_account_id(account_id=topup.account_id, session=session)
    msg = call.message

    if call.data.startswith("topup_confirm__"):
        edits = {}
        edits['balance_usd' if topup.balance_type == 'usd' else 'balance_uzs'] = (account.balance_usd if topup.balance_type == 'usd' else account.balance_uzs) + topup.amount

        repo.TopUpsTableRepository().edit(conditions={"id": topup_id}, edits={"status": "confirmed"}, session=session)
        repo.AccountsTableRepository().edit(
            conditions={"id": account.id},
            edits=edits,
            session=session
        )

        await call.message.edit_caption(
            caption=f"""{html.bold("#TOP_UP")} #CONFIRMED ✅

 -- To'lov haqida ma'lumot 👇

{html.italic("💳 To'lov turi: " + str(topup.balance_type.upper() + " — " + payment_names[topup.balance_type][topup.payment_type]))}
{html.italic("💰 To'lov summasi: " + str(topup.amount) + ("$" if topup.balance_type.upper() == "usd" else " so'm"))}

 -- Akkaunt va telegram akkaunt haqida ma'lumot 👇

{html.italic("📞 Telefon-raqam: " + str(account.phone_number))}
{html.italic("📧 Elektron-pochta: " + str(account.email))}
{html.italic(msg.caption[msg.caption.index("👤"):])}
"""
        )

        if user:
            await bot.send_message(
                chat_id = user.user_id,
                text = html.bold(f"""To'lov tasdiqlandi, hisobingiz {topup.amount} {'$' if topup.balance_type == 'usd' else " so'm"} ga to'ldirildi ✅""")
            )
    else:
        repo.TopUpsTableRepository().edit(conditions={"id": topup_id}, edits={"status": "denied"}, session=session)

        await call.message.edit_caption(
            caption=f"""{html.bold("#TOP_UP")} #DENIED ❌

 -- To'lov haqida ma'lumot 👇

{html.italic("💳 To'lov turi: " + str(topup.balance_type.upper() + " — " + payment_names[topup.balance_type][topup.payment_type]))}
{html.italic("💰 To'lov summasi: " + str(topup.amount) + ("$" if topup.balance_type.upper() == "usd" else " so'm"))}

 -- Akkaunt va telegram akkaunt haqida ma'lumot 👇

{html.italic("📞 Telefon-raqam: " + str(account.phone_number))}
{html.italic("📧 Elektron-pochta: " + str(account.email))}
{html.italic(msg.caption[msg.caption.index("👤"):])}
""",
        )

        if user:
            await bot.send_message(
                chat_id = user.user_id,
                text = html.bold("To'lov tasdiqlanmadi, shikoyatlaringiz bo'lsa administratorga murojaat qiling ❌")
            )