from aiogram import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message

from messages import MESSAGES


def get_main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    my_projects_button = KeyboardButton("🗄 Мои предложения 🗄")
    search_projects_button = KeyboardButton("💰 Поиск предложений 💰")
    markup.add(my_projects_button, search_projects_button)
    return markup


async def start_cmd(message: Message):
    await message.answer(text=MESSAGES['start'].format(message.from_user), reply_markup=get_main_keyboard())


async def back_to_main_menu(message: Message):
    await message.answer(text=MESSAGES['main_menu'].format(message.from_user), reply_markup=get_main_keyboard())


def register_main_handlers(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=['start'])
    dp.register_message_handler(back_to_main_menu, text=['Вернуться в главное меню'])
