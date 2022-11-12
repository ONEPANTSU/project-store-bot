from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from data_base.db_functions import get_moderator_id
from handlers.moderator.moderator_functions import check_is_admin, check_is_moderator
from texts.buttons import BUTTONS
from texts.messages import MESSAGES


def get_main_keyboard(is_moderator=False):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    my_projects_button = KeyboardButton(BUTTONS["sell_menu"])
    search_projects_button = KeyboardButton(BUTTONS["buy_menu"])
    information_button = KeyboardButton(
        BUTTONS["information"], url=MESSAGES["inform_url"]
    )
    if is_moderator:
        moderator_button = KeyboardButton(BUTTONS["moderate"])
        settings_button = KeyboardButton(BUTTONS["settings"])
        markup.add(
            moderator_button,
            settings_button,
            search_projects_button,
        )
    else:
        markup.add(my_projects_button, search_projects_button, information_button)
    return markup


async def main_menu(message, message_text):
    is_moderator = check_is_moderator(message.from_user.id)
    await message.answer(
        text=message_text,
        reply_markup=get_main_keyboard(is_moderator=is_moderator),
    )
