from aiogram.dispatcher.filters.state import State, StatesGroup


class SellProjectStates(StatesGroup):
    seller = State()
    project_name = State()
    price = State()
    price2 = State()
    subscribers = State()
    themes_names = State()
    themes_plus = State()
    income = State()
    comment = State()
    confirm = State()
