from aiogram.fsm.state import State, StatesGroup


class EditProfile(StatesGroup):
    waiting_for_name = State()
    waiting_for_surname = State()
    waiting_for_email = State()
    waiting_for_phone_number = State()
