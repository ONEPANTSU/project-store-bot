from aiogram.types import CallbackQuery

from data_base.db_functions import get_guarantee_name
from handlers.seller.inner_functions.seller_carousel_keyboard import get_my_projects_keyboard
from texts.messages import MESSAGES
from useful.instruments import bot


async def update_project_page(query: CallbackQuery, project_list, page):
    keyboard, project_info = get_page_content(page, project_list)
    await query.message.edit_text(
        text=project_info,
        reply_markup=keyboard,
    )


async def create_project_page(chat_id, project_list, page):
    keyboard, project_info = get_page_content(page, project_list)
    await bot.send_message(
        chat_id=chat_id,
        text=project_info,
        parse_mode="HTML",
        reply_markup=keyboard,
    )


def get_page_content(page, project_list):
    project_info = create_project_info(project_list[page])
    keyboard = get_my_projects_keyboard(project_list=project_list, page=page)
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
        guarantee=guarantee,
    )
    return project_info


def get_themes_str(themes_names):
    themes_str = ""
    for theme_name in themes_names:
        themes_str += "#" + str(theme_name) + " "
    return themes_str
