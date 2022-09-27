from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from handlers.main_handlers import get_main_keyboard
from messages import MESSAGES


async def buy_menu(message: Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    category_button = KeyboardButton("Выбрать тематику")
    price_range_button = KeyboardButton("Выбрать ценовой диапазон")
    back_button = KeyboardButton("Вернуться в главное меню")
    markup.add(category_button, price_range_button, back_button)
    await message.answer(text=MESSAGES['buy_menu'].format(message.from_user), reply_markup=markup)


async def chose_themes(message: Message):
    await message.answer(text=MESSAGES['chose_themes'].format(message.from_user), reply_markup=get_main_keyboard())


async def chose_prices(message: Message):
    await message.answer(text=MESSAGES['chose_prices'].format(message.from_user),
                         reply_markup=get_main_keyboard())


def register_buy_handlers(dp: Dispatcher):
    dp.register_message_handler(buy_menu, text=["💰 Поиск предложений 💰"])
    dp.register_message_handler(chose_themes, text=['Выбрать тематику'])
    dp.register_message_handler(chose_prices, text=['Выбрать ценовой диапазон'])
