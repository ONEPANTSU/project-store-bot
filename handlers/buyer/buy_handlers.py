from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, KeyboardButton, Message, ReplyKeyboardMarkup

from data_base.db_functions import get_project_list_by_filter
from handlers.buyer.buy_callbacks import buy_project_callback, themes_callback
from handlers.buyer.buy_functions import (
    buy_menu,
    buy_project_index,
    chose_themes_keyboard,
    get_buy_projects_price_keyboard,
    get_project_info,
    show_main_buy_keyboard,
)
from handlers.main.main_functions import get_main_keyboard, main_menu
from states import BuyProjectStates
from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.messages import MESSAGES
from useful.commands_handler import commands_handler
from useful.instruments import bot


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


async def search_project_by_button(message: Message):
    await show_main_buy_keyboard(message)


async def search_project_by_command(message: Message):
    await show_main_buy_keyboard(message)


# Действия по нажатию кнопки Выбрать параметры поиска
async def chose_search_parameters(message: Message):
    # await BuyProjectStates.question_price.set()
    await message.answer(
        text=MESSAGES["question_price"].format(message.from_user),
        reply_markup=yes_no_menu(),
    )
    await BuyProjectStates.question_price.set()  # Вызов состояния вопроса про цену


# Вопрос про цену
async def question_price_state(message: Message, state: FSMContext):
    answer = message.text
    if answer.lstrip("/") in COMMANDS.values():
        await state.finish()
        await commands_handler(message)
    elif answer == "Да" or answer == "Нет":
        await state.update_data(price_ans=answer)
        await message.answer(
            text=MESSAGES["question_theme"].format(message.from_user),
            reply_markup=yes_no_menu(),
        )
        await BuyProjectStates.analyse_answers.set()
    else:
        await message.answer(
            text=MESSAGES["yes_or_no"].format(message.from_user),
            reply_markup=yes_no_menu(),
        )
        await BuyProjectStates.question_price.set()  # Вызов состояния вопроса про цену


# Вопрос про тему и
# Анализ введенных ответов и дальнейший вывод
async def analyse_answers_state(message: Message, state: FSMContext):
    answer = message.text
    if answer.lstrip("/") in COMMANDS.values():
        await state.finish()
        await commands_handler(message)
    elif answer == "Да" or answer == "Нет":
        await state.update_data(theme_ans=answer)
        data = await state.get_data()
        price_ans = data["price_ans"]
        theme_ans = data["theme_ans"]

        if price_ans == "Нет" and theme_ans == "Да":
            await message.answer(
                text=MESSAGES["themes_list_smile"], reply_markup=buy_menu()
            )
            await message.answer(
                text=MESSAGES["themes_list"], reply_markup=chose_themes_keyboard()
            )
            await state.finish()

        elif price_ans == "Да" and theme_ans == "Нет":
            await message.answer(
                text=MESSAGES["chose_price_from"], reply_markup=buy_menu()
            )
            await BuyProjectStates.price_from.set()

        elif price_ans == "Да" and theme_ans == "Да":
            await message.answer(
                text=MESSAGES["chose_price_from"], reply_markup=buy_menu()
            )
            await BuyProjectStates.price_from.set()

        elif price_ans == "Нет" and theme_ans == "Нет":
            await message.answer(text=MESSAGES["all_projects"], reply_markup=buy_menu())
            await buy_project_index(
                chat_id=message.chat.id,
                theme_id="None",
                price_from="None",
                price_up_to="None",
            )
            await state.finish()
    else:
        await message.answer(
            text=MESSAGES["yes_or_no"].format(message.from_user),
            reply_markup=yes_no_menu(),
        )
        await BuyProjectStates.analyse_answers.set()


async def back_to_buy_menu(message: Message):
    answer = message.text
    if answer.lstrip("/") in COMMANDS.values():
        await commands_handler(message)
    elif answer == BUTTONS["back_to_buy_menu"]:
        await bot.send_message(
            chat_id=message.chat.id, text=MESSAGES["buy_menu"], reply_markup=buy_menu()
        )


# Получение ответа про цену "от" и запрос цены "до"
async def price_from_state(message: Message, state: FSMContext):
    answer = message.text
    if answer.lstrip("/") in COMMANDS.values():
        await state.finish()
        await commands_handler(message)
    elif answer == BUTTONS["chose_search_params"]:
        await chose_search_parameters(message)
        return 0
    elif answer == BUTTONS["back"]:
        await main_menu(message, message_text=MESSAGES["main_menu"])
        await state.finish()
        return 0

    elif answer.isdigit() and int(answer) >= 0:
        await state.update_data(price_from=answer)
        await message.answer(MESSAGES["chose_price_up_to"])
        await BuyProjectStates.price_up_to.set()
    else:
        await message.answer(
            text=MESSAGES["error_not_digit_price_from"].format(message.from_user),
            reply_markup=buy_menu(),
        )
        await BuyProjectStates.price_from.set()


async def price_up_to_state(message: Message, state: FSMContext):
    answer = message.text
    if answer.lstrip("/") in COMMANDS.values():
        await state.finish()
        await commands_handler(message)
    elif answer == BUTTONS["chose_search_params"]:
        await chose_search_parameters(message)
        await state.finish()
        return 0
    elif answer == BUTTONS["back"]:
        await main_menu(message, message_text=MESSAGES["main_menu"])
        return 0
    data = await state.get_data()
    if answer.isdigit() and int(answer) >= 0:
        if int(answer) >= int(data["price_from"]):
            await state.update_data(price_up_to=answer)
            price_from = data["price_from"]
            price_up_to = answer
            theme_ans = data["theme_ans"]

            if theme_ans == "Нет":
                # Если только цена, то вывод следующий(отправляю в колбэк только цены)
                await buy_project_index(
                    chat_id=message.chat.id,
                    theme_id="None",
                    price_from=price_from,
                    price_up_to=price_up_to,
                )

            elif theme_ans == "Да":
                await message.reply(
                    text=MESSAGES["themes_list"],
                    reply_markup=chose_themes_keyboard(price_from, price_up_to),
                )  # вывод клавы тем
            await state.finish()
        else:
            await message.answer(
                text=MESSAGES["error_upto_bigger_then_from"].format(message.from_user),
                reply_markup=buy_menu(),
            )
            await BuyProjectStates.price_up_to.set()
    else:
        await message.answer(
            text=MESSAGES["error_not_digit_price_upto"].format(message.from_user),
            reply_markup=buy_menu(),
        )
        await BuyProjectStates.price_up_to.set()


async def buy_project_index_by_callback(query: CallbackQuery, callback_data: dict):
    theme_id = callback_data.get("theme_id")
    price_from = callback_data.get("price_from")
    price_up_to = callback_data.get("price_up_to")
    await buy_project_index(query.message.chat.id, theme_id, price_from, price_up_to)
    await bot.answer_callback_query(query.id)


async def buy_project_page_handler(query: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    theme_id = callback_data.get("theme_id")
    price_from = callback_data.get("price_from")
    price_up_to = callback_data.get("price_up_to")
    project_list = get_project_list_by_filter(
        theme_id=theme_id, price_from=price_from, price_up_to=price_up_to
    )
    project_data = project_list[page]
    project_info = get_project_info(project_data=project_data)
    keyboard = get_buy_projects_price_keyboard(
        project_list=project_list,
        theme_id=theme_id,
        price_from=price_from,
        price_up_to=price_up_to,
        page=page,
    )
    await query.message.edit_text(text=project_info, reply_markup=keyboard)
    await bot.answer_callback_query(query.id)


def register_buy_handlers(dp: Dispatcher):
    dp.register_message_handler(get_main_keyboard, text=BUTTONS["back"])
    dp.register_message_handler(search_project_by_button, text=[BUTTONS["buy_menu"]])
    dp.register_message_handler(
        search_project_by_command, commands=[COMMANDS["search_project"]]
    )
    dp.register_message_handler(
        chose_search_parameters, text=[BUTTONS["chose_search_params"]]
    )
    dp.register_message_handler(
        question_price_state, state=BuyProjectStates.question_price
    )
    dp.register_message_handler(
        analyse_answers_state, state=BuyProjectStates.analyse_answers
    )
    dp.register_message_handler(price_from_state, state=BuyProjectStates.price_from)
    dp.register_message_handler(price_up_to_state, state=BuyProjectStates.price_up_to)
    dp.register_callback_query_handler(
        buy_project_index_by_callback, themes_callback.filter()
    )
    dp.register_callback_query_handler(
        buy_project_page_handler, buy_project_callback.filter()
    )
