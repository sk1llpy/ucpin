from aiogram.fsm.state import State, StatesGroup


class PurchaseState(StatesGroup):
    balance_type = State()
    package = State()
    verify = State()
    second_step_verification = State()