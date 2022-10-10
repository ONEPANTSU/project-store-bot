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

from data_base.project import get_guarantee_name, get_project_list_by_filter
from instruments import bot, db_manager
from states import BuyProjectStates
from texts.buttons import BUTTONS
from texts.messages import MESSAGES

buy_project_callback = CallbackData("buy_project_callback", "page", "theme_id", "price_from", "price_up_to")
themes_callback = CallbackData("themes_callback", "theme_id", "price_from", "price_up_to")


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


def back_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    back_button = KeyboardButton(BUTTONS["back_to_buy_menu"])
    markup.add(back_button)
    return markup


async def show_main_buy_keyboard(message: Message):
    await buy_project_index(chat_id=message.chat.id, theme_id="None", price_from="None", price_up_to="None")
    await message.answer(text=MESSAGES["buy_menu"], reply_markup=buy_menu())


# Действия по нажатию кнопки Выбрать параметры поиска
async def chose_search_parameters(message: Message):
    await BuyProjectStates.question_price.set()  # Вызыв состояния вопроса про тему
    await message.answer(text=MESSAGES["question_price"].format(message.from_user), reply_markup=yes_no_menu())
    await BuyProjectStates.question_price.set()  # Вызов состояния вопроса про цену


# Вопрос про цену
async def question_price_state(message: Message, state: FSMContext):
    answer = message.text
    if answer == "Да" or answer == "Нет":
        await state.update_data(price_ans=answer)
        await message.answer(text=MESSAGES["question_theme"].format(message.from_user), reply_markup=yes_no_menu())
        await BuyProjectStates.analyse_answers.set()
    else:
        await message.answer(text=MESSAGES["yes_or_no"].format(message.from_user), reply_markup=yes_no_menu())
        await BuyProjectStates.question_price.set()  # Вызов состояния вопроса про цену

# Вопрос про тему и
# Анализ введенных ответов и дальнейший вывод
async def analyse_answers_state(message: Message, state: FSMContext):
    answer = message.text
    if answer == "Да" or answer == "Нет":
        await state.update_data(theme_ans=answer)
        data = await state.get_data()
        price_ans = data['price_ans']
        theme_ans = data['theme_ans']

        if price_ans == 'Нет' and theme_ans == 'Да':
            await message.reply(text=MESSAGES["themes_list"], reply_markup=chose_themes_keyboard())
            await message.answer(text=MESSAGES["back_to_buy_menu"], reply_markup=back_menu())
            await BuyProjectStates.back_to_buy_menu.set()
            await state.finish()

        elif price_ans == 'Да' and theme_ans == 'Нет':
            await message.answer(text=MESSAGES["chose_price_from"], reply_markup=back_menu())
            await BuyProjectStates.price_from.set()

        elif price_ans == 'Да' and theme_ans == 'Да':
            await message.answer(text=MESSAGES["chose_price_from"], reply_markup=back_menu())
            await BuyProjectStates.price_from.set()
    else:
        await message.answer(text=MESSAGES["yes_or_no"].format(message.from_user), reply_markup=yes_no_menu())
        await BuyProjectStates.analyse_answers.set()


async def back_to_buy_menu_state(message: Message, state: FSMContext):
    answer = message.text
    if answer == BUTTONS['back_to_buy_menu']:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["buy_menu"],
            reply_markup=buy_menu())
    await state.finish()


# Получение ответа про цену "от" и запрос цены "до"
async def price_from_state(message: Message, state: FSMContext):
    answer = message.text
    if answer == BUTTONS['back_to_buy_menu']:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["buy_menu"],
            reply_markup=buy_menu())
        await state.finish()
    elif answer.isdigit():
        await state.update_data(price_from=answer)
        await message.answer(MESSAGES["chose_price_up_to"])
        await BuyProjectStates.price_up_to.set()
    else:
        await message.answer(text=MESSAGES["error_not_digit_price_from"].format(message.from_user), reply_markup=yes_no_menu())
        await BuyProjectStates.price_from.set()


async def price_up_to_state(message: Message, state: FSMContext):
    answer = message.text
    if answer == BUTTONS['back_to_buy_menu']:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["buy_menu"],
            reply_markup=buy_menu())
        await state.finish()
    if answer.isdigit():
        await state.update_data(price_up_to=answer)
        data = await state.get_data()
        price_from = data["price_from"]
        price_up_to = data["price_up_to"]
        theme_ans = data["theme_ans"]

        if theme_ans == "Нет":
            # Если только цена, то вывод следующий(отправляю в колбэк только цены
            await buy_project_index(chat_id=message.chat.id, theme_id="None", price_from=price_from, price_up_to=price_up_to)

        elif theme_ans == "Да":
            await message.reply(text=MESSAGES["themes_list"], reply_markup=chose_themes_keyboard(price_from, price_up_to)) # вывод клавы тем
        await state.finish()

    else:
        await message.answer(text=MESSAGES["error_not_digit_price_upto"].format(message.from_user), reply_markup=yes_no_menu())
        await BuyProjectStates.price_up_to.set()


def chose_themes_keyboard(price_from="None", price_up_to="None"):
    # С помощью функции get_all_themes() присваиваем в themes - словарь с темами и их айди
    themes = db_manager.get_filled_themes()
    # button_list = []
    themes_keyboard = InlineKeyboardMarkup(row_width=2)
    # Заполнение списка тем из словаря с базы данных
    for theme_key in themes.keys():
        themes_keyboard.add(
            InlineKeyboardButton(
                text=themes[theme_key],
                callback_data=themes_callback.new(theme_id="{}".format(theme_key), price_from=price_from, price_up_to=price_up_to)
            )
        )
    return themes_keyboard


# Клавиатура для карусели по листу проектов
def get_buy_projects_price_keyboard(project_list, theme_id, price_from, price_up_to, page: int = 0) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    has_next_page = len(project_list) > page + 1

    page_num_button = InlineKeyboardButton(
        text=f"{page + 1} / {len(project_list)}", callback_data="dont_click_me"
    )

    back_button = InlineKeyboardButton(
        text=BUTTONS["prev"], callback_data=buy_project_callback.new(page=page - 1,
                                                                     theme_id=theme_id,
                                                                     price_from=price_from,
                                                                     price_up_to=price_up_to)
    )

    next_button = InlineKeyboardButton(
        text=BUTTONS["next"], callback_data=buy_project_callback.new(page=page + 1,
                                                                     theme_id=theme_id,
                                                                     price_from=price_from,
                                                                     price_up_to=price_up_to)
    )

    keyboard.row(page_num_button)

    if page != 0:
        if has_next_page:
            keyboard.row(back_button, next_button)
        else:
            keyboard.row(back_button)
    elif has_next_page:
        keyboard.row(next_button)

    return keyboard


# # Обновление страниц в карусели
# async def refresh_pages(query: CallbackQuery, callback_data: dict):
#     page = int(callback_data.get("page"))
#     price_from = int(callback_data.get("price_from"))
#     price_up_to = int(callback_data.get("price_up_to"))
#     project_list = get_project_list_by_filter(price_from, price_up_to)
#     if len(project_list) != 0:
#         project_data = project_list[page]
#         guarantee = get_guarantee_name()
#         themes_str = ""
#         for theme_name in project_data.themes_names:
#             themes_str += "#" + str(theme_name) + " "
#         project_info = MESSAGES["show_project"].format(
#             name=project_data.name,
#             theme=themes_str,
#             subs=project_data.subscribers,
#             income=project_data.income,
#             comm=project_data.comment,
#             seller=project_data.seller_name,
#             price=project_data.price,
#             guarantee=guarantee,
#         )
#         keyboard = get_bye_projects_price_keyboard(project_list=project_list, page=page)
#
#         await query.message.edit_text(text=project_info, reply_markup=keyboard)
#     else:
#         await query.message.edit_text(
#             text=MESSAGES["empty_projects"], reply_markup=None
#         )



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


async def buy_project_index_by_callback(query: CallbackQuery, callback_data: dict):
    theme_id = callback_data.get("theme_id")
    price_from = callback_data.get("price_from")
    price_up_to = callback_data.get("price_up_to")
    await buy_project_index(query.message.chat.id, theme_id, price_from, price_up_to)
    await bot.answer_callback_query(query.id)


async def buy_project_index(chat_id, theme_id, price_from, price_up_to):
    project_list = get_project_list_by_filter(themes_id=theme_id, price_from=price_from, price_up_to=price_up_to)
    project_data = project_list[0]
    project_info = get_project_info(project_data=project_data)
    keyboard = get_buy_projects_price_keyboard(project_list=project_list, theme_id=theme_id, price_from=price_from,
                                               price_up_to=price_up_to)
    await bot.send_message(
        chat_id=chat_id,
        text=project_info,
        parse_mode="HTML",
        reply_markup=keyboard,
    )


async def buy_project_page_handler(query: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    theme_id = callback_data.get("theme_id")
    price_from = callback_data.get("price_from")
    price_up_to = callback_data.get("price_up_to")
    project_list = get_project_list_by_filter(themes_id=theme_id, price_from=price_from, price_up_to=price_up_to)
    project_data = project_list[page]
    project_info = get_project_info(project_data=project_data)
    keyboard = get_buy_projects_price_keyboard(project_list=project_list,
                                               theme_id=theme_id,
                                               price_from=price_from,
                                               price_up_to=price_up_to,
                                               page=page)
    await query.message.edit_text(text=project_info, reply_markup=keyboard)
    await bot.answer_callback_query(query.id)


def register_buy_handlers(dp: Dispatcher):
    dp.register_message_handler(show_main_buy_keyboard, text=[BUTTONS["buy_menu"]])
    # dp.register_message_handler(chose_prices, text=[BUTTONS["buy_price_range"]])
    dp.register_message_handler(chose_search_parameters, text=[BUTTONS["chose_search_params"]])
    dp.register_message_handler(question_price_state, state=BuyProjectStates.question_price)
    dp.register_message_handler(analyse_answers_state, state=BuyProjectStates.analyse_answers)
    dp.register_message_handler(price_from_state, state=BuyProjectStates.price_from)
    dp.register_message_handler(price_up_to_state, state=BuyProjectStates.price_up_to)
    dp.register_message_handler(back_to_buy_menu_state,state=BuyProjectStates.back_to_buy_menu)
    dp.register_callback_query_handler(buy_project_index_by_callback, themes_callback.filter())
    dp.register_callback_query_handler(buy_project_page_handler, buy_project_callback.filter())

