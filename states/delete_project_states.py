from aiogram.dispatcher.filters.state import State, StatesGroup


class DeleteProjectStates(StatesGroup):
    confirm = State()
