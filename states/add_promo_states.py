from aiogram.dispatcher.filters.state import State, StatesGroup


class AddPromoStates(StatesGroup):
    type = State()
    discount = State()
    code = State()
    confirm = State()
