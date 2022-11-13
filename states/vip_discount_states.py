from aiogram.dispatcher.filters.state import State, StatesGroup


class VipDiscountStates(StatesGroup):
    is_need = State()
    code = State()
