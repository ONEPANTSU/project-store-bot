from aiogram.dispatcher.filters.state import StatesGroup, State


class BuyProjectStates(StatesGroup):
    question_theme = State()
    question_price = State()
    analys_answers = State()


    price_from = State()
    price_up_to = State()