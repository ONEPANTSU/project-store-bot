from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from data_base.project import get_projects_list_by_theme_id, get_guarantee_name
from handlers.main_handlers import get_main_keyboard
from texts.buttons import BUTTONS
from texts.messages import MESSAGES
from instruments import db_manager, dp, bot


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
        themes_keyboard.add(
            InlineKeyboardButton(text=themes[i], callback_data="ch_ct{}".format(i)))  # Если не выйдет то эту версию
        # button_list.append(InlineKeyboardButton(text=themes[i], callback_data="ch_ct{}".format(i)))

    # сборка клавиатуры из кнопок `InlineKeyboardButton`
    await message.reply(text=MESSAGES['chose_themes'], reply_markup=themes_keyboard)


@dp.callback_query_handler(lambda c: c.data)
async def theme_callback_handler(callback_query: CallbackQuery):
    theme_id = int(callback_query.data[5:])
    projects_list = get_projects_list_by_theme_id(theme_id)

    for project in projects_list:
        themes_str = ''
        guarantee = get_guarantee_name()
        for i in project.themes_names:
            themes_str += "#" + str(i) + ' '
        project_info = MESSAGES['show_project'].format(
                                   name=project.name,
                                   theme=themes_str,
                                   subs=project.subscribers,
                                   income=project.income,
                                   comm=project.comment,
                                   seller=project.seller_name,
                                   price=project.price,
                                   guarantee=guarantee)
        await bot.send_message(callback_query.message.chat.id, project_info)
    await bot.answer_callback_query(callback_query.id)


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
