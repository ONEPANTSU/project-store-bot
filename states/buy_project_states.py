from aiogram.dispatcher.filters.state import State, StatesGroup


class BuyProjectStates(StatesGroup):
    question_theme = State()
    question_price = State()
    analyse_answers = State()
    price_from = State()
    price_up_to = State()
