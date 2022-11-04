from aiogram.types import Message

from data_base.db_functions import get_regular_sell_price, get_vip_sell_price
from handlers.seller.inner_functions.seller_keyboard_markups import (
    get_back_menu_keyboard,
    get_main_sell_keyboard,
)
from handlers.seller.instruments.seller_dicts import projects_in_moderation
from states import SellProjectStates
from texts.messages import MESSAGES
from useful.instruments import bot


async def put_up_for_sale(message: Message):
    if message.from_user.username is not None:
        if message.chat.id in projects_in_moderation:
            await bot.send_message(
                chat_id=message.chat.id,
                text=MESSAGES["already_in_moderation"],
                reply_markup=get_main_sell_keyboard(),
            )
        else:
            await message.answer(text=MESSAGES["put_up_for_sale"].format(regular_price=
                                                                         str(int(int(get_regular_sell_price())/100)),
                                                                         vip_price=str(int(int(get_regular_sell_price() +
                                                                                       get_vip_sell_price())/100))))
            await message.answer(
                text=MESSAGES["project_name"], reply_markup=get_back_menu_keyboard()
            )
            await SellProjectStates.project_name.set()
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["empty_username"],
            reply_markup=get_main_sell_keyboard(),
        )
