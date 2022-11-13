from aiogram.dispatcher.filters.state import State, StatesGroup


class DiscountStates(StatesGroup):
    is_need = State()
    code = State()
