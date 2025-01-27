from aiogram.fsm.state import State, StatesGroup


class TopUpState(StatesGroup):
    balance_type = State()
    payment_type = State()
    amount = State()
    cheque = State()