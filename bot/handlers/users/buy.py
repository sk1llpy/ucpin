import time

from aiogram import types, F, html
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session

from bot.decorators import create_session
from bot.keyboards.inline import purchase, menu
from bot.misc import bot, bot_settings
from bot.routers import users
from bot.states.purchase import PurchaseState
from bot.filters.ban import IsBanned
from db import repository as repo


@users.callback_query(IsBanned(), F.data == 'menu__purchase')
@create_session
async def menu_purchase_handler(call: types.CallbackQuery, state: FSMContext, session: Session):
    await state.set_state(PurchaseState.balance_type)
    await call.message.edit_text(
        text=html.bold("Kerakli bo'limni tanlang 👇"),
        reply_markup=await purchase.balance_type()
    )
    

@users.callback_query(IsBanned(), F.data.in_(["purchase__USD", "purchase__UZS", "back__to_menu"]), StateFilter(PurchaseState.balance_type))
@create_session
async def purchase_balance_type_handler(call: types.CallbackQuery, state: FSMContext, session: Session):
    if not call.data == "back__to_menu":
        await state.update_data(balance_type = ("usd" if call.data.endswith("USD") else "uzs"))
        await state.set_state(PurchaseState.package)
        
        await call.message.edit_text(
            text=html.bold("Kerakli uc paketni tanlang 👇"),
            reply_markup=await purchase.packages(call.data.split("__")[1].lower(), session)
        )
    else:
        await call.message.edit_text(
            text = html.bold("Kerakli bo'limni tanlang 👇"),
            reply_markup = await menu.button()
        )

        await state.clear()


@users.callback_query(IsBanned(), F.data.startswith("purchase__"), StateFilter(PurchaseState.package))
@create_session
async def purchase_package_handler(call: types.CallbackQuery, state: FSMContext, session: Session):
    if not call.data == "purchase__back_balance_type":
        package_id = call.data.split("__")[1]

        try:
            package_id: int = int(package_id)
        except TypeError:
            return

        data = await state.get_data()
        balance_type = data['balance_type']
        
        package_obj = await repo.UCPackagesTableRepository().get_ucpackage_by_id(
            package_id = package_id,
            session = session
        )

        reedem_codes = await repo.RedeemCodesTableRepository().get_active_redeem_codes_by_package_id(
            package_id = package_id,
            session = session
        )

        if reedem_codes:
            await state.update_data(package_id = package_id, package = package_obj, max_count = len(reedem_codes), count = 1)
            await state.set_state(PurchaseState.verify)
            
            await call.message.edit_text(
                text=f"""{html.bold("Siz tanlagan paket:")} {package_obj.title}

{html.italic("Qolgan redeem-kod'lar soni:")} {len(reedem_codes)}""",
                reply_markup=await purchase.counter()
            )

        else:
            await call.message.edit_text(
                text = html.bold("Uzr") + ", ushbu UC paketi hozirda faol emas yoki barcha redeem-kod'lar tugagan. 😔",
                reply_markup=await purchase.packages(balance_type, session)
            )
    else:
        await state.set_state(PurchaseState.balance_type)
        await call.message.edit_text(
            text=html.bold("Kerakli bo'limni tanlang 👇"),
            reply_markup=await purchase.balance_type()
        )


# Counter
@users.callback_query(IsBanned(), F.data == "plus", StateFilter(PurchaseState.verify))
async def purchase_counter_plus_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current = int(call.message.reply_markup.inline_keyboard[0][1].text)
    await state.update_data(count = current)
    
    if current < data.get("max_count"):
        await call.message.edit_reply_markup(reply_markup=await purchase.counter(current + 1))
    else:
        await call.answer(
            text="😔 " + "Afsus!" + " Hozirda boshqa Redeem-kodlar qolmagan."
        )


@users.callback_query(IsBanned(), F.data == "minus", StateFilter(PurchaseState.verify))
async def purchase_counter_minus_handler(call: types.CallbackQuery, state: FSMContext):
    current = int(call.message.reply_markup.inline_keyboard[0][1].text)
    await state.update_data(count = current)

    if current > 1:
        await call.message.edit_reply_markup(reply_markup=await purchase.counter(current - 1))


# Confirm
@users.callback_query(IsBanned(), F.data.in_(["purchase__back_to_uc_package", "purchase__confirm"]), StateFilter(PurchaseState.verify))
@create_session
async def purchase_confirm_handler(call: types.CallbackQuery, state: FSMContext, session: Session):   
    data = await state.get_data()
    balance_type = data.get('balance_type')

    if not call.data == "purchase__back_to_uc_package":
        package = data.get('package')
        current = int(call.message.reply_markup.inline_keyboard[0][1].text)

        total_price = (package.price_usd * current) if balance_type == 'usd' else (package.price_uzs * current)

        await state.update_data(count = current, total_price = total_price)
        await state.set_state(PurchaseState.second_step_verification)

        await call.message.edit_text(
            text = html.bold(f"""Siz rostdan ham {current} ta {package.title} ni {total_price} {"$" if balance_type == "usd" else "so'm"} ga harid qilmoqchimisiz?"""),
            reply_markup = await purchase.confirm()
        )
    else:
        await state.set_state(PurchaseState.package)
        
        await call.message.edit_text(
            text=html.bold("Kerakli uc paketni tanlang 👇"),
            reply_markup=await purchase.packages(balance_type, session)
        )
        


@users.callback_query(IsBanned(), F.data == "purchase__yes", StateFilter(PurchaseState.second_step_verification))
@create_session
async def purchase_confirm_yes_handler(call: types.CallbackQuery, state: FSMContext, session: Session):
    data = await state.get_data()
    account = await repo.UsersTableRepository().get_user_account(user_id=call.from_user.id, session=session)

    count = data.get('count')
    package = data.get('package')
    package_id = data.get('package_id')
    total_price = data.get('total_price')
    balance_type = data.get('balance_type')
    redeem_codes = await repo.RedeemCodesTableRepository().get_active_redeem_codes_by_package_id(package_id=package.id, session=session)

    if (account.balance_usd if balance_type == 'usd' else account.balance_uzs) >= total_price:
        if len(redeem_codes) >= count:
            sended_message = await call.message.edit_text(
                text=f"""{html.bold("Harid muvvafaqiyatli amalga oshirildi ✅")}

{html.italic("🛍 UC Paket: " + str(package.title))}
{html.italic("🔄 Soni: " + str(count) + " ta")}
{html.italic("💰 Jami: " + str(total_price) + ("$" if balance_type == 'usd' else " so'm"))}

{html.italic("Redeem-kod'lar 👇")}\n"""
            )

            redeem_codes = redeem_codes[:count]
            text = sended_message.text + "\n"
            num = 0
            redeem_codes_text = "<b>Redeem-kod'lar 👇</b>\n"

            for redeem_code in redeem_codes:
                await repo.PurchasesTableRepository().purchase(
                    account_id = account.id,
                    balance_type = balance_type,
                    redeem_code_id = redeem_code.id,
                    session = session
                )

                num += 1
                text += "\n" + f"{num}. " + html.code(redeem_code.code)
                redeem_codes_text += "\n" + f"{num}. " + html.code(redeem_code.code)

                await sended_message.edit_text(text = text)

                time.sleep(0.1)
            
            edits = {}
            edits['balance_usd' if balance_type == 'usd' else 'balance_uzs'] = (account.balance_usd if balance_type == 'usd' else account.balance_uzs) - total_price

            repo.AccountsTableRepository().edit(
                conditions = {"id": account.id},
                edits = edits,
                session = session
            )
            
            await call.message.answer(
                text = """<b>Kerakli bo'limni tanlang 👇</b>""",
                reply_markup = await menu.button()
            )

            admin_chat_msg = await bot.send_message(
                chat_id = bot_settings.admin_group,
                text = f"""{html.bold("#PURCHASE ✅")}

 -- Akkaunt va telegram akkaunt haqida ma'lumot 👇

{html.italic("📞 Telefon-raqam: " + str(account.phone_number))}
{html.italic("📧 Elektron-pochta: " + str(account.email))}
{html.italic("👤 To'liq ismi: " + call.from_user.full_name)}
{html.italic("🆔 Telegram ID: " + str(call.from_user.id))}
{html.italic("👤 Username: " + "@" + str(call.from_user.username))}

 -- To'lov haqida ma'lumot 👇

{html.italic("🛍 UC Paket: " + str(package.title))}
{html.italic("🔄 Soni: " + str(count) + " ta")}
{html.italic("💰 Jami: " + str(total_price) + ("$" if balance_type == 'usd' else " so'm"))}"""
            )
            await admin_chat_msg.reply(text = redeem_codes_text)

            await state.clear()
        else:
            await state.clear()

            await call.message.edit_text(
                text = html.bold("Afsuski") + ", bizda yetarli redeem-code'lar qolmadi. Harid bekor qilindi ❌",
                reply_markup = await menu.button()
            )
    else:
        await state.clear()

        await call.message.edit_text(
            text = html.bold("Afsuski") + ", sizning balansingizda yetarli mablag' mavjud emas. Harid bekor qilindi ❌",
            reply_markup = await menu.button()
        )


@users.callback_query(IsBanned(), F.data == "purchase__no", StateFilter(PurchaseState.second_step_verification))
@create_session
async def purchase_confirm_no_handler(call: types.CallbackQuery, state: FSMContext, session: Session):
    await state.clear()

    await call.message.edit_text(
        text = html.bold("Harid bekor qilindi ❌") + "\n\n" + html.italic("Kerakli bo'limni tanlang 👇"),
        reply_markup = await menu.button()
    )


@users.callback_query(IsBanned(), F.data == "purchase__back_to_counter", StateFilter(PurchaseState.second_step_verification))
@create_session
async def purchase_back_to_counter_handler(call: types.CallbackQuery, state: FSMContext, session: Session):
    data = await state.get_data()

    package_id = data.get('package_id')
    balance_type = data['balance_type']
    count = data['count']
    
    package_obj = await repo.UCPackagesTableRepository().get_ucpackage_by_id(package_id = package_id, session = session)
    reedem_codes = await repo.RedeemCodesTableRepository().get_active_redeem_codes_by_package_id(package_id = package_id, session = session)

    await state.set_state(PurchaseState.verify)
    await call.message.edit_text(
        text=f"""{html.bold("Siz tanlagan paket:")} {package_obj.title}

{html.italic("Qolgan redeem-kod'lar soni:")} {len(reedem_codes)}""",
        reply_markup=await purchase.counter(count)
    )