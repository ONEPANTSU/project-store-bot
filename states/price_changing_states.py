from aiogram.dispatcher.filters.state import State, StatesGroup


class PriceChangingStates(StatesGroup):
    price = State()
    confirm = State()
