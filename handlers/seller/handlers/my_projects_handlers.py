from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from data_base.db_functions import get_projects_list_by_seller_name
from handlers.main_handlers import get_main_keyboard
from handlers.seller.inner_functions.seller_carousel_pages import (
    get_delete_project_dict_info,
    refresh_pages, my_project_index,
)
from handlers.seller.inner_functions.seller_keyboard_markups import (
    get_main_sell_keyboard,
    get_project_confirmation_menu_keyboard,
)
from handlers.seller.instruments.seller_callbacks import (
    delete_project_callback,
    my_projects_callback,
)
from handlers.seller.instruments.seller_dicts import delete_project_dict, is_moderator_dict
from states import DeleteProjectStates
from texts.buttons import BUTTONS
from texts.messages import MESSAGES
from useful.instruments import bot, db_manager


async def my_project_index_handler(message: Message):
    project_list = get_projects_list_by_seller_name(message.from_user.username)
    await my_project_index(message=message, project_list=project_list, is_moderator=False)


async def my_project_page_handler(query: CallbackQuery, callback_data: dict):
    await refresh_pages(query=query, callback_data=callback_data)


async def delete_project_handler(query: CallbackQuery, callback_data: dict):
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=MESSAGES["confirm_deleting"],
        reply_markup=get_project_confirmation_menu_keyboard(back_button=False),
    )
    is_moderator_str = callback_data.get("is_moderator")
    if is_moderator_str == "True":
        is_moderator = True
    else:
        is_moderator = False
    is_moderator_dict[query.message.chat.id] = is_moderator
    delete_project_dict[query.message.chat.id] = [
        int(callback_data.get("id")),
        query,
        callback_data,
    ]
    await DeleteProjectStates.confirm.set()


async def delete_confirm_handler(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(confitrm=answer)
    await check_delete_confirm(answer, message, state)


async def check_delete_confirm(answer, message, state):
    if answer == BUTTONS["confirm"]:
        await confirmed_deleting(message, state)
    elif answer == BUTTONS["cancellation"]:
        await canceled_deleting(message, state)
    else:
        await deleting_command_error(message)


async def deleting_command_error(message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=MESSAGES["command_error"],
        reply_markup=get_project_confirmation_menu_keyboard(),
    )
    await DeleteProjectStates.confirm.set()


async def canceled_deleting(message, state):
    if is_moderator_dict[message.chat.id]:
        reply_markup = get_main_keyboard(is_moderator=is_moderator_dict[message.chat.id])
    else:
        reply_markup = get_main_sell_keyboard()
        await my_project_index_handler(message=message)
    is_moderator_dict.pop(message.chat.id)
    await bot.send_message(
        chat_id=message.chat.id,
        text=MESSAGES["not_deleted_project"],
        reply_markup=reply_markup,
    )
    delete_project_dict.pop(message.chat.id)
    await state.finish()


async def confirmed_deleting(message, state):
    callback_data, project_id, query = get_delete_project_dict_info(message.chat.id)
    db_manager.delete_project(project_id)
    if is_moderator_dict[message.chat.id]:
        reply_markup = get_main_keyboard(is_moderator=is_moderator_dict[message.chat.id])
    else:
        reply_markup = get_main_sell_keyboard()
    is_moderator_dict.pop(message.chat.id)
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=MESSAGES["deleted_project"],
        reply_markup=reply_markup,
    )
    await refresh_pages(query=query, callback_data=callback_data)
    await state.finish()


def register_my_projects_handlers(dp: Dispatcher):
    dp.register_message_handler(my_project_index_handler, text=BUTTONS["sell_list"])
    dp.register_callback_query_handler(
        my_project_page_handler, my_projects_callback.filter()
    )
    dp.register_callback_query_handler(
        delete_project_handler, delete_project_callback.filter()
    )
    dp.register_message_handler(
        delete_confirm_handler, state=DeleteProjectStates.confirm
    )
