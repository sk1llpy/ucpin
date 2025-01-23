from aiogram.fsm.state import State, StatesGroup

class RegisterState(StatesGroup):
    action = State()
    
    # Register
    phone_number = State()
    email = State()
    password = State()
    
    # Login
    phone_number_or_email = State()
    login_password = State()