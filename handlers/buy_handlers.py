from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from handlers.main_handlers import get_main_keyboard
from texts.buttons import BUTTONS
from texts.messages import MESSAGES


async def buy_menu(message: Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    themes_button = KeyboardButton(BUTTONS['buy_chose_themes'])
    price_range_button = KeyboardButton(BUTTONS['buy_price_range'])
    back_button = KeyboardButton(BUTTONS['back'])
    markup.add(themes_button, price_range_button, back_button)
    await message.answer(text=MESSAGES['buy_menu'].format(message.from_user), reply_markup=markup)


async def chose_themes(message: Message):
    await message.answer(text=MESSAGES['chose_themes'].format(message.from_user), reply_markup=get_main_keyboard())


async def chose_prices(message: Message):
    await message.answer(text=MESSAGES['chose_prices'].format(message.from_user),
                         reply_markup=get_main_keyboard())


def register_buy_handlers(dp: Dispatcher):
    dp.register_message_handler(buy_menu, text=[BUTTONS['buy_menu']])
    dp.register_message_handler(chose_themes, text=[BUTTONS['buy_chose_themes']])
    dp.register_message_handler(chose_prices, text=[BUTTONS['buy_price_range']])
