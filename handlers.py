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


@dp.message_handler(text=['🗄 Мои предложения 🗄'])
async def show_main_sell_keyboard(message: Message):
    await message.answer(text=MESSAGES['sell_menu'].format(message.from_user), reply_markup=show_main_sell_keyboard())


def show_main_sell_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    to_sell_project_button = KeyboardButton("Выставить проект на продажу")
    list_of_my_projects_button = KeyboardButton("Список моих предложений")
    back_button = KeyboardButton("Вернуться в главное меню")
    markup.add(to_sell_project_button, list_of_my_projects_button, back_button)
    return markup


@dp.message_handler(text=['Выставить проект на продажу'])
async def put_up_for_sale(message: Message):
    await message.answer(text=MESSAGES['put_up_for_sale'].format(message.from_user), reply_markup=get_main_keyboard())


@dp.message_handler(text=['Список моих предложений'])
async def get_list_of_projects(message: Message):
    await message.answer(text=MESSAGES['get_list_of_projects'].format(message.from_user), reply_markup=get_main_keyboard())


@dp.message_handler(text=['Вернуться в главное меню'])
async def back_to_main_menu(message: Message):
    await message.answer(text=MESSAGES['main_menu'].format(message.from_user), reply_markup=get_main_keyboard())

