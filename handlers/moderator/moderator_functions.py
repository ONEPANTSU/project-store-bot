from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data_base.db_functions import get_moderator_id, get_admin_id
from texts.buttons import BUTTONS


def check_is_moderator(user_id):
    is_moderator = False
    if user_id == get_moderator_id() or user_id == get_admin_id():
        is_moderator = True
    return is_moderator


def check_is_current_moderator(user_id):
    is_moderator = False
    if user_id == get_moderator_id():
        is_moderator = True
    return is_moderator


def check_is_admin(user_id):
    is_admin = False
    if user_id == get_admin_id():
        is_admin = True
    return is_admin


def get_settings_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    moderators_button = KeyboardButton(BUTTONS["moderators"])
    payment_button = KeyboardButton(BUTTONS["payment"])
    promo_button = KeyboardButton(BUTTONS["promo"])
    guarantee_button = KeyboardButton(BUTTONS["guarantee"])
    back_button = KeyboardButton(BUTTONS["back"])
    markup.row(moderators_button, payment_button)
    markup.row(promo_button, guarantee_button)
    markup.row(back_button)
    return markup


def get_moderators_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    back_button = KeyboardButton(BUTTONS["back"])
    markup.row(back_button)
    return markup


def get_admin_moderators_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    add_moderator_button = KeyboardButton(BUTTONS["add_moderator"])
    back_button = KeyboardButton(BUTTONS["back"])
    markup.row(add_moderator_button)
    markup.row(back_button)
    return markup
