from aiogram.dispatcher.filters.state import State, StatesGroup


class BuyProjectStates(StatesGroup):
    chose_search_parameters = State()
    back_to_buy_menu = State()

    question_price = State()
    analyse_answers = State()

    price_from = State()
    price_up_to = State()
