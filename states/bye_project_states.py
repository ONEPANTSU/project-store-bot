from aiogram.dispatcher.filters.state import StatesGroup, State


class ByeProjectStates(StatesGroup):
    price_from = State()
    price_up_to = State()