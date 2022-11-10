from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from data_base.db_functions import get_moderators_info
from handlers.moderator.moderator_callback import delete_moderator_callback, moderator_page_callback, \
    chose_moderator_callback
from handlers.moderator.moderator_functions import check_is_moderator
from texts.buttons import BUTTONS
from texts.messages import MESSAGES
from useful.instruments import bot


async def refresh_moderator_pages(query: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    moderator_list = get_moderators_info()
    await update_moderator_page(page, moderator_list, query)


async def update_moderator_page(page, project_list, query):
    if len(project_list) != 0:
        await edit_moderator_page(
            query=query, project_list=project_list, page=page
        )
    else:
        await query.message.edit_text(
            text="Список модераторов пуст! :с", reply_markup=None
        )


async def edit_moderator_page(query: CallbackQuery, project_list, page):
    keyboard, moderator_name = get_moderator_page_content(page, project_list)
    await query.message.edit_text(
        text=moderator_name,
        reply_markup=keyboard,
    )


async def moderators_index(message: Message):
    moderator_list = get_moderators_info()
    if len(moderator_list) != 0:
        await create_moderator_page(
            chat_id=message.chat.id,
            moderator_list=moderator_list,
            page=0
        )
    else:
        await bot.send_message(chat_id=message.chat.id, text=MESSAGES["empty_projects"])


async def create_moderator_page(chat_id, moderator_list, page):
    keyboard, moderator_name = get_moderator_page_content(page, moderator_list)
    await bot.send_message(
        chat_id=chat_id,
        text=moderator_name,
        parse_mode="HTML",
        reply_markup=keyboard,
    )


def get_moderator_page_content(page, moderator_list):
    moderator_name = moderator_list[page][1]
    keyboard = get_moderator_page_keyboard(
        moderator_list=moderator_list, page=page
    )
    return keyboard, moderator_name


def get_moderator_page_keyboard(moderator_list, page):
    has_next_page = len(moderator_list) > page + 1
    page_num_button = create_page_num_button(page, len(moderator_list))
    delete_button = create_delete_button(page, moderator_list)
    back_button = create_back_button(page)
    next_button = create_next_button(page)
    if check_is_moderator(moderator_list[page][0]):
        current_moderator_button = create_current_moderator_button()
        return create_current_moderator_page(
            has_next_page, page_num_button, back_button, next_button, current_moderator_button, page
        )
    else:
        chose_moderator_button = create_chose_moderator_button(moderator_list[page][0])
        return create_other_moderator_page(
            has_next_page, page_num_button, delete_button, back_button, next_button, chose_moderator_button, page
        )


def create_other_moderator_page(
        has_next_page,
        page_num_button,
        delete_button,
        back_button,
        next_button,
        chose_moderator_button,
        page
):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(page_num_button)
    keyboard.row(delete_button)
    keyboard.row(chose_moderator_button)
    return add_page_buttons(has_next_page, keyboard, back_button, next_button, page)


def create_current_moderator_page(
        has_next_page,
        page_num_button,
        back_button,
        next_button,
        current_moderator_button,
        page
):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(page_num_button)
    keyboard.row(current_moderator_button)
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


def create_current_moderator_button():
    return InlineKeyboardButton(
        text=BUTTONS["current_moderator"],
        callback_data="current_moderator_dont_click_me"
    )


def create_chose_moderator_button(moderator_id):
    return InlineKeyboardButton(
        text=BUTTONS["chose_moderator"],
        callback_data=chose_moderator_callback.new(
            id=moderator_id
        ),
    )


def create_next_button(page):
    return InlineKeyboardButton(
        text=BUTTONS["next"],
        callback_data=moderator_page_callback.new(
            page=page + 1
        ),
    )


def create_back_button(page):
    return InlineKeyboardButton(
        text=BUTTONS["prev"],
        callback_data=moderator_page_callback.new(
            page=page - 1
        ),
    )


def create_delete_button(page, moderator_list):
    return InlineKeyboardButton(
        text=BUTTONS["delete_moderator"],
        callback_data=delete_moderator_callback.new(
            id=moderator_list[page][0], page=0
        ),
    )


def create_page_num_button(page, moderator_list_len):
    return InlineKeyboardButton(
        text=f"{page + 1} / {moderator_list_len}", callback_data="dont_click_me"
    )
