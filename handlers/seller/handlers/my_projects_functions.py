from aiogram.types import Message

from data_base.db_functions import get_moderator_id, get_projects_list_by_seller_name
from handlers.seller.inner_functions.seller_carousel_pages import my_project_index


async def my_project_index_handler(message: Message):
    project_list = get_projects_list_by_seller_name(message.from_user.username)
    is_moderator = False
    if message.from_user.id == get_moderator_id():
        is_moderator = True
    await my_project_index(
        message=message, project_list=project_list, is_moderator=is_moderator
    )
