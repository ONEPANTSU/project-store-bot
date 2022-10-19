from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from handlers.seller.instruments.seller_callbacks import (
    delete_project_callback,
    my_projects_callback,
    vip_project_callback,
)
from texts.buttons import BUTTONS


def get_my_projects_keyboard(
    project_list, is_moderator, page: int = 0
) -> InlineKeyboardMarkup:
    has_next_page = len(project_list) > page + 1

    page_num_button = create_page_num_button(page, len(project_list))
    delete_button = create_delete_button(page, project_list, is_moderator)
    back_button = create_back_button(page, is_moderator)
    next_button = create_next_button(page, is_moderator)

    if project_list[page].status_id == 0 and (not is_moderator):
        vip_button = create_vip_button(page, project_list, is_moderator)
        return create_my_regular_projects_keyboard(
            back_button,
            delete_button,
            vip_button,
            has_next_page,
            next_button,
            page,
            page_num_button,
        )
    else:
        return create_my_vip_projects_keyboard(
            back_button,
            delete_button,
            has_next_page,
            next_button,
            page,
            page_num_button,
        )


def create_my_regular_projects_keyboard(
    back_button,
    delete_button,
    vip_button,
    has_next_page,
    next_button,
    page,
    page_num_button,
):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(page_num_button)
    keyboard.row(delete_button)
    keyboard.row(vip_button)
    return add_page_buttons(has_next_page, keyboard, back_button, next_button, page)


def create_my_vip_projects_keyboard(
    back_button, delete_button, has_next_page, next_button, page, page_num_button
):
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


def create_next_button(page, is_moderator):
    return InlineKeyboardButton(
        text=BUTTONS["next"],
        callback_data=my_projects_callback.new(
            page=page + 1, is_moderator=is_moderator
        ),
    )


def create_back_button(page, is_moderator):
    return InlineKeyboardButton(
        text=BUTTONS["prev"],
        callback_data=my_projects_callback.new(
            page=page - 1, is_moderator=is_moderator
        ),
    )


def create_delete_button(page, project_list, is_moderator):
    return InlineKeyboardButton(
        text=BUTTONS["delete_project"],
        callback_data=delete_project_callback.new(
            id=project_list[page].id, page=0, is_moderator=is_moderator
        ),
    )


def create_vip_button(page, project_list, is_moderator):
    return InlineKeyboardButton(
        text=BUTTONS["vip_project"],
        callback_data=vip_project_callback.new(
            id=project_list[page].id, page=page, is_moderator=is_moderator
        ),
    )


def create_page_num_button(page, project_list_len):
    return InlineKeyboardButton(
        text=f"{page + 1} / {project_list_len}", callback_data="dont_click_me"
    )
