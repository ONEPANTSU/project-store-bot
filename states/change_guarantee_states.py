from aiogram.dispatcher.filters.state import State, StatesGroup


class ChangeGuaranteeStates(StatesGroup):
    ask = State()
    confirm = State()
