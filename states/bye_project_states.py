from aiogram.dispatcher.filters.state import State, StatesGroup


class ByeProjectStates(StatesGroup):
    price_from = State()
    price_up_to = State()
