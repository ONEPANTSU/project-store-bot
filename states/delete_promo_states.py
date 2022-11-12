from aiogram.dispatcher.filters.state import State, StatesGroup


class DeletePromoStates(StatesGroup):
    confirm = State()
