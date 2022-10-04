from aiogram import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.messages import MESSAGES


def get_main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    my_projects_button = KeyboardButton(BUTTONS['sell_menu'])
    search_projects_button = KeyboardButton(BUTTONS['buy_menu'])
    markup.add(my_projects_button, search_projects_button)
    return markup


async def start_cmd(message: Message):
    await message.answer(text=MESSAGES['start'].format(message.from_user), reply_markup=get_main_keyboard())


async def back_by_button(message: Message):
    await back_to_main_menu(message)


async def back_by_command(message: Message):
    await back_to_main_menu(message)


async def back_to_main_menu(message: Message):
    await message.answer(text=MESSAGES['main_menu'].format(message.from_user), reply_markup=get_main_keyboard())


def register_main_handlers(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=[COMMANDS['start']])
    dp.register_message_handler(back_by_button, text=[BUTTONS['back']])
    dp.register_message_handler(back_by_command, commands=[COMMANDS['back']])
