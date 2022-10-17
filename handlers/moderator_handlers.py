from aiogram import Dispatcher
from aiogram.types import Message

from data_base.db_functions import get_all_project_list, get_moderator_id
from handlers.seller.inner_functions.seller_carousel_pages import my_project_index
from texts.buttons import BUTTONS


async def moderator_handler(message: Message):
    is_moderator = False
    if message.from_user.id == get_moderator_id():
        is_moderator = True
    if is_moderator:
        project_list = get_all_project_list()
        await my_project_index(message=message, project_list=project_list, is_moderator=is_moderator)


def register_moderator_handlers(dp: Dispatcher):
    dp.register_message_handler(moderator_handler, text=BUTTONS["moderate"])
