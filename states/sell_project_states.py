from aiogram.dispatcher.filters.state import StatesGroup, State


class SellProjectStates(StatesGroup):
    project_name = State()
    price = State()
    price2 = State()
    subscribers = State()
    themes_names = State()
    themes_plus = State()
    income = State()
    comment = State()
