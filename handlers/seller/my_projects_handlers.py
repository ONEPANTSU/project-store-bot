from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from aiogram.utils.callback_data import CallbackData

from data_base.db_functions import get_guarantee_name, get_projects_list_by_seller_name
from handlers.seller.seller_keyboard_markups import (
    get_main_sell_keyboard,
    get_project_confirmation_menu_keyboard,
)
from instruments import bot, db_manager
from states import DeleteProjectStates
from texts.buttons import BUTTONS
from texts.messages import MESSAGES

delete_project_dict = {}
my_projects_callback = CallbackData("my_projects", "page")
delete_project_callback = CallbackData("delete_project", "id", "page")


def get_my_projects_keyboard(project_list, page: int = 0) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    has_next_page = len(project_list) > page + 1

    page_num_button = InlineKeyboardButton(
        text=f"{page + 1} / {len(project_list)}", callback_data="dont_click_me"
    )

    delete_button = InlineKeyboardButton(
        text=BUTTONS["delete_project"],
        callback_data=delete_project_callback.new(id=project_list[page].id, page=0),
    )

    back_button = InlineKeyboardButton(
        text=BUTTONS["prev"], callback_data=my_projects_callback.new(page=page - 1)
    )

    next_button = InlineKeyboardButton(
        text=BUTTONS["next"], callback_data=my_projects_callback.new(page=page + 1)
    )

    keyboard.row(page_num_button)
    keyboard.row(delete_button)
    if page != 0:
        if has_next_page:
            keyboard.row(back_button, next_button)
        else:
            keyboard.row(back_button)
    elif has_next_page:
        keyboard.row(next_button)

    return keyboard


async def my_project_index(message: Message):
    project_list = get_projects_list_by_seller_name(message.from_user.username)
    if len(project_list) != 0:
        project_data = project_list[0]
        keyboard = get_my_projects_keyboard(project_list=project_list)  # Page: 0
        guarantee = get_guarantee_name()
        themes_str = ""
        for theme_name in project_data.themes_names:
            themes_str += "#" + str(theme_name) + " "
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
        await bot.send_message(
            chat_id=message.chat.id,
            text=project_info,
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    else:
        await bot.send_message(chat_id=message.chat.id, text=MESSAGES["empty_projects"])


async def my_project_page_handler(query: CallbackQuery, callback_data: dict):
    await refresh_pages(query=query, callback_data=callback_data)


async def delete_project_handler(query: CallbackQuery, callback_data: dict):
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=MESSAGES["confirm_deleting"],
        reply_markup=get_project_confirmation_menu_keyboard(back_button=False),
    )
    delete_project_dict[query.message.chat.id] = [
        int(callback_data.get("id")),
        query,
        callback_data,
    ]
    await DeleteProjectStates.confirm.set()


async def delete_confirm(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(confitrm=answer)
    if answer == BUTTONS["confirm"]:
        project_id = delete_project_dict[message.chat.id][0]
        query = delete_project_dict[message.chat.id][1]
        callback_data = delete_project_dict[message.chat.id][2]
        db_manager.delete_project(project_id)
        await bot.send_message(
            chat_id=query.message.chat.id,
            text=MESSAGES["deleted_project"],
            reply_markup=get_main_sell_keyboard(),
        )
        await refresh_pages(query=query, callback_data=callback_data)

        delete_project_dict.pop(message.chat.id)
        await state.finish()

    elif answer == BUTTONS["cancellation"]:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["not_deleted_project"],
            reply_markup=get_main_sell_keyboard(),
        )
        await my_project_index(message=message)
        delete_project_dict.pop(message.chat.id)
        await state.finish()

    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["command_error"],
            reply_markup=get_project_confirmation_menu_keyboard(),
        )
        await DeleteProjectStates.confirm.set()


async def refresh_pages(query: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))

    project_list = get_projects_list_by_seller_name(query.from_user.username)
    if len(project_list) != 0:
        project_data = project_list[page]
        guarantee = get_guarantee_name()
        themes_str = ""
        for theme_name in project_data.themes_names:
            themes_str += "#" + str(theme_name) + " "
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
        keyboard = get_my_projects_keyboard(project_list=project_list, page=page)

        await query.message.edit_text(text=project_info, reply_markup=keyboard)
    else:
        await query.message.edit_text(
            text=MESSAGES["empty_projects"], reply_markup=None
        )


def register_my_projects_handlers(dp: Dispatcher):
    dp.register_message_handler(my_project_index, text=BUTTONS["sell_list"])
    dp.register_callback_query_handler(
        my_project_page_handler, my_projects_callback.filter()
    )
    dp.register_callback_query_handler(
        delete_project_handler, delete_project_callback.filter()
    )
    dp.register_message_handler(delete_confirm, state=DeleteProjectStates.confirm)
