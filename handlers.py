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

