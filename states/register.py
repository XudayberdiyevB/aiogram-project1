from aiogram.dispatcher.filters.state import State, StatesGroup


class RegisterForm(StatesGroup):
    region = State()
    city = State()
