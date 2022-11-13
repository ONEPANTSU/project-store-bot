from aiogram.dispatcher.filters.state import State, StatesGroup


class ChangePaymentStates(StatesGroup):
    ask = State()
    regular = State()
    vip = State()
    confirm = State()
    switch = State()
