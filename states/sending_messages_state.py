from aiogram.dispatcher.filters.state import State, StatesGroup


class SendingMessagesStates(StatesGroup):
    write = State()
    confirm = State()
