from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
from aiogram.utils.callback_data import CallbackData

from data_base.project import get_guarantee_name, get_projects_list_by_theme_id
from instruments import bot, db_manager
from states import BuyProjectStates
from texts.buttons import BUTTONS
from texts.messages import MESSAGES

buy_project_callback = CallbackData("buy_project_callback", "page", "theme_id")
themes_callback = CallbackData("themes_callback", "data")


def buy_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    chose_search_params = KeyboardButton(BUTTONS["chose_search_params"])
    back_button = KeyboardButton(BUTTONS["back"])
    markup.add(chose_search_params, back_button)
    return markup


def yes_no_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    yes_button = KeyboardButton(BUTTONS["yes"])
    no_button = KeyboardButton(BUTTONS["no"])
    markup.add(yes_button, no_button)
    return markup


async def show_main_buy_keyboard(message: Message):
    # где-то ориентировочно тут надо вставить функцию выводаchose_search_params всех проектов
    await message.answer(text=MESSAGES["buy_menu"], reply_markup=buy_menu())
    # где-то ориентировочно тут надо вставить функцию вывода всех проектов
    await message.answer(text=MESSAGES["buy_menu"].format(message.from_user), reply_markup=buy_menu())


# Действия по нажатию кнопки Выбрать параметры поиска
async def chose_search_parameters(message: Message):
    await BuyProjectStates.question_price.set()  # Вызыв состояния вопроса про тему
    await message.answer(text=MESSAGES["question_price"].format(message.from_user), reply_markup=yes_no_menu())
    await BuyProjectStates.question_price.set()  # Вызов состояния вопроса про цену


# Вопрос про цену
async def question_price_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(price_ans=answer)
    await message.answer(text=MESSAGES["question_theme"].format(message.from_user), reply_markup=yes_no_menu())
    await BuyProjectStates.analyse_answers.set()


# Вопрос про тему и
# Анализ введенных ответов и дальнейший вывод
async def analyse_answers_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(theme_ans=answer)
    data = await state.get_data()
    price_ans = data['price_ans']
    theme_ans = data['theme_ans']
    if price_ans == 'Нет' and theme_ans == 'Да':
        await message.answer(text=MESSAGES["chose_themes"], reply_markup=ReplyKeyboardRemove())
        await message.reply(text=MESSAGES["chose_themes"], reply_markup=chose_themes_keyboard())
    elif price_ans == 'Да' and theme_ans == 'Нет':
        pass
    elif price_ans == 'Да' and theme_ans == 'Да':
        pass
    await state.finish()
    # await message.answer(MESSAGES["question_theme"])


def chose_themes_keyboard():
    # С помощью функции get_all_themes() присваиваем в themes - словарь с темами и их айди
    themes = db_manager.get_filled_themes()
    # button_list = []
    themes_keyboard = InlineKeyboardMarkup(row_width=2)
    # Заполнение списка тем из словаря с базы данных
    for theme_key in themes.keys():
        themes_keyboard.add(
            InlineKeyboardButton(
                text=themes[theme_key],
                callback_data=themes_callback.new(data="{}".format(theme_key))
            )
        )
    return themes_keyboard


# Кнопка выбора ценового диапазона
async def chose_prices(message: Message):
    await message.answer(text=MESSAGES["chose_price_from"])
    await BuyProjectStates.price_from.set()


async def price_from_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(price_from=answer)
    await message.answer(MESSAGES["chose_price_up_to"])
    await BuyProjectStates.price_up_to.set()


#  В СЛЕДУЮЩИЙ РАЗ ИРА РАБОТАЕТ ОТСЮДА
# ПС НУЖНА ФУНКЦИЯ ЧТОБЫ ПО СЕРЫМ price_from И price_up_to ВЫТЯНУТЬ ПРОЕКТЫ ИЗ БД
# ПЛЮС СМОТРИ ЗАДАЧКИ В ЗАМЕТНИКЕ
async def price_up_to_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(price_up_to=answer)
    data = await state.get_data()
    price_from = data["price_from"]
    price_up_to = data["price_up_to"]
    await state.finish()


def get_buy_projects_keyboard(
    project_list, theme_id, page: int = 0
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    has_next_page = len(project_list) > page + 1

    keyboard.add(
        InlineKeyboardButton(
            text=f"{page + 1} / {len(project_list)}", callback_data="dont_click_me"
        )
    )

    if page != 0:
        keyboard.add(
            InlineKeyboardButton(
                text="< Назад",
                callback_data=buy_project_callback.new(
                    page=page - 1, theme_id=theme_id
                ),
            )
        )

    if has_next_page:
        keyboard.add(
            InlineKeyboardButton(
                text="Вперёд >",
                callback_data=buy_project_callback.new(
                    page=page + 1, theme_id=theme_id
                ),
            )
        )

    return keyboard


def get_project_info(project_data):  # Page: 0
    guarantee = get_guarantee_name()
    themes_str = ""
    for theme_name in project_data.themes_names:
        themes_str += "#" + str(theme_name) + " "
    project_info = MESSAGES["show_project"].format(
        name=project_data.name,
        theme=themes_str,
        subs=project_data.subscribers,
        income=project_data.income,
        comm=project_data.comment,
        seller=project_data.seller_name,
        price=project_data.price,
        guarantee=guarantee,
    )
    return project_info


async def buy_project_index(query: CallbackQuery, callback_data: dict):
    theme_id = callback_data.get("data")
    project_list = get_projects_list_by_theme_id(theme_id)
    project_data = project_list[0]
    project_info = get_project_info(project_data=project_data)
    keyboard = get_buy_projects_keyboard(project_list=project_list, theme_id=theme_id)
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=project_info,
        parse_mode="HTML",
        reply_markup=keyboard,
    )
    await bot.answer_callback_query(query.id)


async def buy_project_page_handler(query: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    theme_id = int(callback_data.get("theme_id"))
    project_list = get_projects_list_by_theme_id(theme_id)
    project_data = project_list[page]
    project_info = get_project_info(project_data=project_data)
    keyboard = get_buy_projects_keyboard(
        project_list=project_list, theme_id=theme_id, page=page
    )
    await query.message.edit_text(text=project_info, reply_markup=keyboard)
    await bot.answer_callback_query(query.id)


def register_buy_handlers(dp: Dispatcher):
    dp.register_message_handler(show_main_buy_keyboard, text=[BUTTONS["buy_menu"]])
    dp.register_message_handler(chose_prices, text=[BUTTONS["buy_price_range"]])
    dp.register_message_handler(chose_search_parameters, text=[BUTTONS["chose_search_params"]])
    dp.register_message_handler(question_price_state, state=BuyProjectStates.question_price)
    dp.register_message_handler(analyse_answers_state, state=BuyProjectStates.analyse_answers)
    dp.register_message_handler(price_from_state, state=BuyProjectStates.price_from)
    dp.register_message_handler(price_up_to_state, state=BuyProjectStates.price_up_to)
    dp.register_callback_query_handler(buy_project_index, themes_callback.filter())
    dp.register_callback_query_handler(buy_project_page_handler, buy_project_callback.filter())
