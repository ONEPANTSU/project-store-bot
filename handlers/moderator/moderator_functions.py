from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from data_base.db_functions import get_admin_id, get_all_promo_codes, get_moderator_id
from handlers.moderator.moderator_callback import (
    add_promo_callback,
    delete_promo_callback,
)
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


def get_promo_type_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    rub_button = KeyboardButton("₽")
    percent_button = KeyboardButton("%")
    back_button = KeyboardButton(BUTTONS["cancellation"])
    markup.row(rub_button, percent_button)
    markup.row(back_button)
    return markup


def get_promo_keyboard():
    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    promo_list = get_all_promo_codes()
    for promo in promo_list:
        code = promo.rpartition("\t~\t")[0]
        new_delete_button = InlineKeyboardButton(
            text="❌\t" + promo + "\t❌",
            callback_data=delete_promo_callback.new(
                code=code,
            ),
        )
        markup.row(new_delete_button)
    add_button = InlineKeyboardButton(
        text=BUTTONS["add_promo"], callback_data=add_promo_callback.new()
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


def get_payment_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    change_regular_price_button = KeyboardButton(BUTTONS["change_regular_price"])
    change_vip_price_button = KeyboardButton(BUTTONS["change_vip_price"])
    switch_payment_button = KeyboardButton(BUTTONS["switch_payment"])
    cancellation_button = KeyboardButton(BUTTONS["cancellation"])
    markup.row(change_regular_price_button)
    markup.row(change_vip_price_button)
    markup.row(switch_payment_button)
    markup.row(cancellation_button)
    return markup
