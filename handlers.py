from aiogram.types import Message, LabeledPrice, \
    PreCheckoutQuery, ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.message import ContentType
from messages import MESSAGES
from config import PAYMENTS_TOKEN
from main import dp, bot
from data_base.db_manager import DBManager

db_manager = DBManager()


def get_main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    my_projects_button = KeyboardButton("🗄 Мои предложения 🗄")
    search_projects_button = KeyboardButton("💰 Поиск предложений 💰")
    markup.add(my_projects_button, search_projects_button)
    return markup


@dp.message_handler(commands=['start'])
async def start_cmd(message: Message):
    await message.answer(text=MESSAGES['start'].format(message.from_user), reply_markup=get_main_keyboard())


@dp.message_handler(text=["💰 Поиск предложений 💰"])
async def buy_menu(message: Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    category_button = KeyboardButton("Выбрать тематику")
    price_range_button = KeyboardButton("Выбрать ценовой диапазон")
    back_button = KeyboardButton("Вернуться в главное меню")
    markup.add(category_button, price_range_button, back_button)
    await message.answer(text=MESSAGES['buy_menu'].format(message.from_user), reply_markup=markup)


