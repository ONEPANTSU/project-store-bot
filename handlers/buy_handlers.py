from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove,\
    KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from handlers.main_handlers import get_main_keyboard
from texts.buttons import BUTTONS
from texts.messages import MESSAGES
from instruments import db_manager, dp


async def buy_menu(message: Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    themes_button = KeyboardButton(BUTTONS['buy_chose_themes'])
    price_range_button = KeyboardButton(BUTTONS['buy_price_range'])
    back_button = KeyboardButton(BUTTONS['back'])
    markup.add(themes_button, price_range_button, back_button)
    await message.answer(text=MESSAGES['buy_menu'], reply_markup=markup)


async def chose_themes(message: Message):
    # С помощью функции get_all_themes() присваиваем в themes - словарь с темами и их айди
    themes = db_manager.get_all_themes()
    # button_list = []
    themes_keyboard = InlineKeyboardMarkup(row_width=2)
    # Заполнение списка тем из словаря с базы данных
    for i in themes.keys():
        themes_keyboard.add(InlineKeyboardButton(text=themes[i], callback_data="ch_ct{}".format(i)))
        # button_list.append(InlineKeyboardButton(text=themes[i], callback_data="ch_ct{}".format(i)))
    # сборка клавиатуры из кнопок `InlineKeyboardButton`


    await message.reply(text=MESSAGES['chose_themes'], reply_markup=themes_keyboard)


async def theme_callback_handler(call):
    theme_id = int(call.data[5:])
    proj = db_manager.get_projects_info_by_theme_id(theme_id)
    await dp.send_message(call.message.chat.id, 'Data: {}'.format(proj))
    await dp.answer_callback_query(call.id)


# Функция построения меню в сообщении
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


async def chose_prices(message: Message):
    await message.answer(text=MESSAGES['chose_prices'], reply_markup=get_main_keyboard())


def register_buy_handlers(dp: Dispatcher):
    dp.register_message_handler(buy_menu, text=[BUTTONS['buy_menu']])
    dp.register_message_handler(chose_themes, text=[BUTTONS['buy_chose_themes']])
    dp.register_message_handler(chose_prices, text=[BUTTONS['buy_price_range']])
    dp.register_callback_query_handler(theme_callback_handler, lambda callback_query: True)

