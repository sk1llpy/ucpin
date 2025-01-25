import re

from aiogram import types, F, html
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from sqlalchemy.orm import Session

from bot.decorators import create_session
from bot.keyboards.default import register
from bot.keyboards.inline import login, menu
from bot.misc import bot
from bot.routers import users
from bot.filters.ban import IsBanned
from bot.states.register import RegisterState
from db import repository as repo

email_regexp = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'


@users.callback_query(F.data.in_(['login', 'register']), StateFilter(RegisterState.action))
@create_session
async def action_register_handler(call: types.CallbackQuery, state: FSMContext, session: Session):
    user_account = await repo.UsersTableRepository().get_user_account(user_id=call.from_user.id, session=session)

    if not user_account: 
        if call.data == 'register':
            await state.set_state(RegisterState.phone_number)
            await call.message.delete()

            msg_for_delete = await call.message.answer(
                text = html.bold("Ro'yxatdan o'tish uchun telefon raqamingizni yuboring 📞"),
                reply_markup = await register.phone_number()
            )
        else:
            await state.set_state(RegisterState.phone_number_or_email)
            await call.message.edit_text(
                text = html.bold("Hisobga kirish uchun elektron-pochtangizni yoki telefon raqamingizni kiriting 👇")
            )


# Register
@users.message(F.content_type == types.ContentType.CONTACT, StateFilter(RegisterState.phone_number))
@create_session
async def phone_number_register_handler(message: types.Message, state: FSMContext, session: Session):
    phone_number = message.contact.phone_number
    phone_number = ("+" + str(phone_number)) if not phone_number.startswith("+") else phone_number

    phone_number_exists = await repo.AccountsTableRepository().check_phone_number_exists(phone_number=phone_number, session=session)

    if not phone_number_exists:
        if phone_number.startswith("+998"):
            await state.update_data({"phone_number": phone_number})
            await state.set_state(RegisterState.email)

            await message.reply(
                text=html.bold("Telefon raqamingiz muvvafaqiyatli qo'shildi ✅"),
                reply_markup=types.ReplyKeyboardRemove()
            )
            await message.answer(
                text=html.bold("Elektron-pochtangizni kiriting 📧")
            )
        else:
            await message.reply(text=html.bold("Telefon raqam +998 bilan boshlanishi kerak ❌"))
    else:
        await message.reply(text=html.bold("Ushbu telefon raqam allaqachon mavjud ❌"))


@users.message(F.content_type == types.ContentType.TEXT, StateFilter(RegisterState.email))
@create_session
async def email_register_handler(message: types.Message, state: FSMContext, session: Session):
    email = message.text
    email_is_exists = await repo.AccountsTableRepository().check_email_exists(email=email, session=session)

    if not email_is_exists:
        if re.match(email_regexp, email):
            await state.update_data({"email": email})
            await state.set_state(RegisterState.password)

            await message.reply(
                text=html.bold("Elektron-pochtangiz muvvafaqiyatli qo'shildi ✅"),
                reply_markup=types.ReplyKeyboardRemove()
            )
            await message.answer(
                text=html.bold("Parol yuboring 🔐") + "\n\n" + html.italic("Parol kamida 8 ta harfdan iborat bo'lishi kerak")
            )
        else:
            await message.reply(text=html.bold("Elektron-pochta notog'ri formatda kiritildi ❌"))
    else:
        await message.reply(text=html.bold("Ushbu elektron-pochta allaqachon mavjud ❌"))


@users.message(F.content_type == types.ContentType.TEXT, StateFilter(RegisterState.password))
@create_session
async def password_register_handler(message: types.Message, state: FSMContext, session: Session):
    data = await state.get_data()

    phone_number = data['phone_number']
    email = data['email']
    password = message.text

    account_data = {
        'phone_number': phone_number,
        'email': email,
        'password': password
    }

    account = await repo.AccountsTableRepository().create_account(account_data, session)
    response = await repo.UsersTableRepository().set_account_to_user(
        user_id=message.from_user.id, 
        account_data={
            "email": account.email,
            "password": account.password
        },
        session=session
    )

    await message.reply(html.bold("Akkaunt muvvafaqiyatli yaratildi ✅"))
    await message.answer(
        text=html.bold(f"Salom {message.from_user.first_name} 👋") + "\n\n" +
        html.italic("Kerakli bo'limni tanlang 👇"),
        reply_markup=await menu.button()
    )

    await state.clear()
    

# Login
@users.message(F.content_type == types.ContentType.TEXT, StateFilter(RegisterState.phone_number_or_email))
async def phone_number_or_email_login_handler(message: types.Message, state: FSMContext):
    email_or_phone_number = message.text
    success = False
    
    if email_or_phone_number.startswith("+998"):
        await state.update_data({"phone_number": email_or_phone_number})
        success = True
    elif re.match(email_regexp, email_or_phone_number):
        await state.update_data({"email": email_or_phone_number})
        success = True
    
    if success:
        await state.set_state(RegisterState.login_password)
        
        await message.reply(
            text=html.bold("Ma'lumot muvvafaqiyatli qabul qilindi ✅")
        )
        await message.answer(
            text=html.bold("Parolni kiriting 🔐")
        )
        

@users.message(F.content_type == types.ContentType.TEXT, StateFilter(RegisterState.login_password))
@create_session
async def password_login_handler(message: types.Message, state: FSMContext, session: Session):
    data = await state.get_data()

    phone_number = data.get('phone_number')
    email = data.get('email') if not phone_number else None
    phone_or_email = 'phone_number' if phone_number else 'email'
    password = message.text

    account_data = {"password": password}
    account_data['email' if email else 'phone_number'] = email if email else phone_number

    response: None | dict = await repo.UsersTableRepository().set_account_to_user(
        user_id=message.from_user.id,
        account_data=account_data,
        session=session
    )

    if response:
        if response.get('error') == "ACCOUNT_NOT_FOUND":
            await message.reply(html.bold(f"Akkaunt topilmadi, {'email 'if email else 'telefon-raqam'} yoki parol mos kelmadi!"))
            await state.clear()

            return
        elif response.get('error') == "ACCOUNT_BANNED":
            await message.reply(html.bold("Kirish imkonsiz! Sizning akkauntingiz administrator tomonidan ban qilingan 🚫"))
            await state.clear()

            return
    
    await message.reply(html.bold("Akkauntga muvvafaqiyatli kirildi ✅"))
    await message.answer(
        text=html.bold(f"Salom {message.from_user.first_name} 👋") + "\n\n" +
        html.italic("Kerakli bo'limni tanlang 👇"),
        reply_markup=await menu.button()
    )

    await state.clear()