from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from data_base.db_functions import get_moderator_id, get_admin_id, get_all_promo_codes
from handlers.moderator.moderator_callback import delete_promo_callback, add_promo_callback
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


def get_promo_keyboard():
    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    promo_list = get_all_promo_codes()
    for promo in promo_list:
        new_delete_button = InlineKeyboardButton(
            text="❌\t" + promo + "\t❌",
            callback_data=delete_promo_callback.new(
                code=promo.rpartition(' ~ ')[0],
            )
        )
        markup.row(new_delete_button)
    add_button = InlineKeyboardButton(
        text=BUTTONS["add_promo"],
        callback_data=add_promo_callback.new()
    )
    markup.row(add_button)
    return markup


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


def get_confirmation_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    confirm_button = KeyboardButton(BUTTONS["confirm"])
    cancellation_button = KeyboardButton(BUTTONS["cancellation"])
    markup.row(confirm_button)
    markup.row(cancellation_button)
    return markup


def get_cancel_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    cancellation_button = KeyboardButton(BUTTONS["cancellation"])
    markup.row(cancellation_button)
    return markup
