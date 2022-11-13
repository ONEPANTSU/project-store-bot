from aiogram.dispatcher.filters.state import State, StatesGroup


class AddModeratorStates(StatesGroup):
    id = State()
    name = State()
    confirm = State()
