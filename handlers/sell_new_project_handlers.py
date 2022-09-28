from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from states.sell_project_states import SellProjectStates
from handlers.main_handlers import get_main_keyboard
from messages import MESSAGES


async def sell_new_project(message: Message):
    await message.answer(text=MESSAGES['put_up_for_sale'].format(message.from_user), reply_markup=get_main_keyboard())
    await SellProjectStates.project_name.set()


async def project_name(message: Message):
    await message.answer(text="")


def register_sell_handlers(dp: Dispatcher):
    dp.register_message_handler(sell_new_project, text=['Выставить проект на продажу'])
    dp.register_message_handler(project_name, state=SellProjectStates.project_name)
