from aiogram import Dispatcher
from aiogram.types import Message

from data_base.db_functions import get_all_project_list
from handlers.seller.inner_functions.seller_carousel_pages import my_project_index
from texts.buttons import BUTTONS
from useful.instruments import db_manager


async def moderator_handler(message: Message):
    is_moderator = False
    moderators = db_manager.get_moderators_names()
    for moderator in moderators:
        if message.from_user.id == moderator[0]:
            is_moderator = True
    if is_moderator:
        project_list = get_all_project_list()
        await my_project_index(message=message, project_list=project_list, is_moderator=is_moderator)


def register_moderator_handlers(dp: Dispatcher):
    dp.register_message_handler(moderator_handler, text=BUTTONS["moderate"])
