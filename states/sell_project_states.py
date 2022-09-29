from aiogram.dispatcher.filters.state import StatesGroup, State


class SellProjectStates(StatesGroup):
    project_name = State()
    price = State()
    subscribers = State()
    themes_names = State()
    income = State()
    comment = State()
