from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from handlers.main_handlers import get_main_keyboard
from messages import MESSAGES
from states import SellProjectStates


async def show_main_sell_keyboard(message: Message):
    await message.answer(text=MESSAGES['sell_menu'].format(message.from_user), reply_markup=get_main_sell_keyboard())


def get_main_sell_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    to_sell_project_button = KeyboardButton("Выставить проект на продажу")
    list_of_my_projects_button = KeyboardButton("Список моих предложений")
    back_button = KeyboardButton("Вернуться в главное меню")
    markup.add(to_sell_project_button, list_of_my_projects_button, back_button)
    return markup


async def put_up_for_sale(message: Message):
    await message.answer(text=MESSAGES['put_up_for_sale'].format(message.from_user), reply_markup=get_main_keyboard())
    await SellProjectStates.project_name.set()


async def project_name(message: Message):
    await message.answer(text="")


async def get_list_of_projects(message: Message):
    await message.answer(text=MESSAGES['get_list_of_projects'].format(message.from_user),
                         reply_markup=get_main_keyboard())


def register_sell_handlers(dp: Dispatcher):
    dp.register_message_handler(show_main_sell_keyboard, text=['🗄 Мои предложения 🗄'])
    dp.register_message_handler(put_up_for_sale, text=['Выставить проект на продажу'])
    dp.register_message_handler(project_name, state=SellProjectStates.project_name)
    dp.register_message_handler(get_list_of_projects, text=['Список моих предложений'])
