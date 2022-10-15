from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from texts.buttons import BUTTONS


def get_main_sell_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    to_sell_project_button = KeyboardButton(BUTTONS["sell_project"])
    list_of_my_projects_button = KeyboardButton(BUTTONS["sell_list"])
    back_button = KeyboardButton(BUTTONS["back"])
    markup.add(to_sell_project_button, list_of_my_projects_button, back_button)
    return markup


def get_cancel_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    main_menu_button = KeyboardButton(BUTTONS["back_to_sell_menu"])
    cancel_button = KeyboardButton(BUTTONS["cancel"])
    markup.add(main_menu_button, cancel_button)
    return markup


def get_back_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    back_button = KeyboardButton(BUTTONS["back_to_sell_menu"])
    markup.add(back_button)
    return markup


def get_project_confirmation_menu_keyboard(back_button=True):
    confirm_button = KeyboardButton(BUTTONS["confirm"])
    cancellation_button = KeyboardButton(BUTTONS["cancellation"])
    return create_confirmation_menu_keyboard(
        back_button, cancellation_button, confirm_button
    )


def create_confirmation_menu_keyboard(back_button, cancellation_button, confirm_button):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    if back_button:
        cancel_button = KeyboardButton(BUTTONS["cancel"])
        markup.add(confirm_button, cancellation_button, cancel_button)
    else:
        markup.add(confirm_button, cancellation_button)
    return markup
