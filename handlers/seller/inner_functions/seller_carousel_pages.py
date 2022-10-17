from aiogram.types import CallbackQuery, Message

from data_base.db_functions import get_guarantee_name, get_projects_list_by_seller_name, get_all_project_list
from handlers.seller.inner_functions.seller_carousel_keyboard import (
    get_my_projects_keyboard,
)
from handlers.seller.instruments.seller_dicts import delete_project_dict
from texts.messages import MESSAGES
from useful.instruments import bot


async def my_project_index(message: Message, project_list, is_moderator):
    if len(project_list) != 0:
        await create_project_page(
            chat_id=message.chat.id, project_list=project_list, page=0, is_moderator=is_moderator
        )
    else:
        await bot.send_message(chat_id=message.chat.id, text=MESSAGES["empty_projects"])


async def refresh_pages(query: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    is_moderator_str = callback_data.get("is_moderator")
    if is_moderator_str == "True":
        is_moderator = True
    else:
        is_moderator = False
    if is_moderator:
        project_list = get_all_project_list()
    else:
        project_list = get_projects_list_by_seller_name(query.from_user.username)
    await update_page(page, project_list, query, is_moderator)


async def update_page(page, project_list, query, is_moderator):
    if len(project_list) != 0:
        await edit_project_page(query=query, project_list=project_list, page=page, is_moderator=is_moderator)
    else:
        await query.message.edit_text(
            text=MESSAGES["empty_projects"], reply_markup=None
        )


async def edit_project_page(query: CallbackQuery, project_list, page, is_moderator):
    keyboard, project_info = get_page_content(page, project_list, is_moderator)
    await query.message.edit_text(
        text=project_info,
        reply_markup=keyboard,
    )


async def create_project_page(chat_id, project_list, page, is_moderator):
    keyboard, project_info = get_page_content(page, project_list, is_moderator)
    await bot.send_message(
        chat_id=chat_id,
        text=project_info,
        parse_mode="HTML",
        reply_markup=keyboard,
    )


def get_page_content(page, project_list, is_moderator):
    project_info = create_project_info(project_list[page])
    keyboard = get_my_projects_keyboard(project_list=project_list, page=page, is_moderator=is_moderator)
    return keyboard, project_info


def create_project_info(project_data):
    guarantee = get_guarantee_name()
    themes_str = get_themes_str(project_data.themes_names)
    return get_project_info(project_data, themes_str, guarantee)


def get_project_info(project_data, themes_str, guarantee):
    project_info = MESSAGES["show_project"].format(
        name=project_data.name,
        theme=themes_str,
        subs=project_data.subscribers,
        income=project_data.income,
        comm=project_data.comment,
        seller=project_data.seller_name,
        price=project_data.price,
        link=project_data.link,
        guarantee=guarantee,
    )
    return project_info


def get_themes_str(themes_names):
    themes_str = ""
    for theme_name in themes_names:
        themes_str += "#" + str(theme_name) + " "
    return themes_str


def get_delete_project_dict_info(chat_id):
    project_id = delete_project_dict[chat_id][0]
    query = delete_project_dict[chat_id][1]
    callback_data = delete_project_dict[chat_id][2]
    delete_project_dict.pop(chat_id)
    return callback_data, project_id, query
