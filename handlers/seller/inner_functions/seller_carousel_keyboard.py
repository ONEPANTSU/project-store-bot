from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.seller.instruments.seller_callbacks import my_projects_callback, delete_project_callback
from texts.buttons import BUTTONS


def get_my_projects_keyboard(project_list, page: int = 0) -> InlineKeyboardMarkup:
    has_next_page = len(project_list) > page + 1

    page_num_button = create_page_num_button(page, len(project_list))
    delete_button = create_delete_button(page, project_list)
    back_button = create_back_button(page)
    next_button = create_next_button(page)

    return create_my_projects_keyboard(back_button, delete_button, has_next_page, next_button, page, page_num_button)


def create_my_projects_keyboard(back_button, delete_button, has_next_page, next_button, page,
                                page_num_button):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(page_num_button)
    keyboard.row(delete_button)
    return add_page_buttons(has_next_page, keyboard, back_button, next_button, page)


def add_page_buttons(has_next_page, keyboard, back_button, next_button, page):
    if page != 0:
        if has_next_page:
            keyboard.row(back_button, next_button)
        else:
            keyboard.row(back_button)
    elif has_next_page:
        keyboard.row(next_button)
    return keyboard


def create_next_button(page):
    return InlineKeyboardButton(
        text=BUTTONS["next"], callback_data=my_projects_callback.new(page=page + 1)
    )


def create_back_button(page):
    return InlineKeyboardButton(
        text=BUTTONS["prev"], callback_data=my_projects_callback.new(page=page - 1)
    )


def create_delete_button(page, project_list):
    return InlineKeyboardButton(
        text=BUTTONS["delete_project"],
        callback_data=delete_project_callback.new(id=project_list[page].id, page=0),
    )


def create_page_num_button(page, project_list_len):
    return InlineKeyboardButton(
        text=f"{page + 1} / {project_list_len}", callback_data="dont_click_me"
    )