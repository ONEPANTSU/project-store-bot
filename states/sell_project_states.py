from aiogram.dispatcher.filters.state import StatesGroup, State


class SellProjectStates(StatesGroup):
    project_name = State()
    themes_names = State()