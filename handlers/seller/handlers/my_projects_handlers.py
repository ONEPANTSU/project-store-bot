from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
)

from data_base.db_functions import get_projects_list_by_seller_name
from handlers.seller.inner_functions.seller_carousel_pages import create_project_page, update_project_page
from handlers.seller.instruments.seller_callbacks import my_projects_callback, delete_project_callback
from handlers.seller.instruments.seller_dicts import delete_project_dict
from handlers.seller.inner_functions.seller_keyboard_markups import (
    get_main_sell_keyboard,
    get_project_confirmation_menu_keyboard,
)
from states import DeleteProjectStates
from texts.buttons import BUTTONS
from texts.messages import MESSAGES
from useful.instruments import bot, db_manager


async def my_project_index_handler(message: Message):
    project_list = get_projects_list_by_seller_name(message.from_user.username)
    if len(project_list) != 0:
        await create_project_page(chat_id=message.chat.id, project_list=project_list, page=0)
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
        await my_project_index_handler(message=message)
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
        await update_project_page(query=query, project_list=project_list, page=page)
    else:
        await query.message.edit_text(
            text=MESSAGES["empty_projects"], reply_markup=None
        )


def register_my_projects_handlers(dp: Dispatcher):
    dp.register_message_handler(my_project_index_handler, text=BUTTONS["sell_list"])
    dp.register_callback_query_handler(
        my_project_page_handler, my_projects_callback.filter()
    )
    dp.register_callback_query_handler(
        delete_project_handler, delete_project_callback.filter()
    )
    dp.register_message_handler(delete_confirm, state=DeleteProjectStates.confirm)
