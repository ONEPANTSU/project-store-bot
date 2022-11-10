from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message

from data_base.db_functions import get_moderator_all_project_list, get_moderator_id
from data_base.project import Project
from handlers.seller.inner_functions.seller_carousel_pages import (
    my_project_index,
    refresh_pages,
)
from handlers.seller.instruments.seller_callbacks import verify_callback
from texts.buttons import BUTTONS


async def moderator_handler(message: Message):
    is_moderator = False
    if message.from_user.id == get_moderator_id():
        is_moderator = True
    if is_moderator:
        project_list = get_moderator_all_project_list()
        await my_project_index(
            message=message, project_list=project_list, is_moderator=is_moderator
        )


async def verify_handler(query: CallbackQuery, callback_data: dict):
    is_moderator = callback_data.get("is_moderator")
    if is_moderator:
        project = Project()
        project.set_params_by_id(callback_data.get("id"))
        project.is_verified = 1
        project.save_changes_to_existing_project()
        await refresh_pages(query=query, callback_data=callback_data)


def register_moderator_handlers(dp: Dispatcher):
    dp.register_message_handler(moderator_handler, text=BUTTONS["moderate"])
    dp.register_callback_query_handler(verify_handler, verify_callback.filter())
