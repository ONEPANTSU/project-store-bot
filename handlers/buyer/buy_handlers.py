from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, KeyboardButton, Message, ReplyKeyboardMarkup

from data_base.db_functions import get_project_list_by_filter
from handlers.buyer.buy_callbacks import buy_project_callback, themes_callback, chose_search_params_callback, \
    search_by_theme_params_callback, search_by_price_params_callback
from handlers.buyer.buy_functions import (
    buy_menu,
    buy_project_index,
    chose_themes_keyboard,
    get_buy_projects_keyboard,
    get_project_info,
    show_all_projects,
)
from handlers.main.main_functions import get_main_keyboard, main_menu
from states import BuyProjectStates
from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.messages import MESSAGES
from useful.commands_handler import commands_handler
from useful.instruments import bot


def back_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    back_button = KeyboardButton(BUTTONS["back"])
    markup.add(back_button)
    return markup


async def search_project_by_button(message: Message):
    await show_all_projects(message)


async def search_project_by_command(message: Message):
    await show_all_projects(message)


# Получение ответа про цену "от" и запрос цены "до"
async def price_from_state(message: Message, state: FSMContext):
    answer = message.text
    if answer.lstrip("/") in COMMANDS.values():
        await state.finish()
        await commands_handler(message)
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
    elif answer == BUTTONS["back"]:
        await main_menu(message, message_text=MESSAGES["main_menu"])
        await state.finish()
    data = await state.get_data()
    if answer.isdigit() and int(answer) >= 0:
        if int(answer) >= int(data["price_from"]):
            await state.update_data(price_up_to=answer)
            price_from = data["price_from"]
            price_up_to = answer
            theme_id = data["theme_id"]

            await buy_project_index(
                chat_id=message.chat.id,
                theme_id=theme_id,
                price_from=price_from,
                price_up_to=price_up_to,
            )

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
    # status = int(callback_data.get("status"))
    project_list = get_project_list_by_filter(
        theme_id=theme_id, price_from=price_from, price_up_to=price_up_to
    )
    project_data = project_list[page]
    project_info = get_project_info(project_data=project_data)
    keyboard = get_buy_projects_keyboard(
        project_list=project_list,
        theme_id=theme_id,
        price_from=price_from,
        price_up_to=price_up_to,
        page=page,
        status=0
    )
    await query.message.edit_text(text=project_info, reply_markup=keyboard)
    await bot.answer_callback_query(query.id)


async def chose_params_callback(query: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    theme_id = callback_data.get("theme_id")
    price_from = callback_data.get("price_from")
    price_up_to = callback_data.get("price_up_to")
    status = 1
    project_list = get_project_list_by_filter(
        theme_id=theme_id, price_from=price_from, price_up_to=price_up_to
    )
    project_data = project_list[page]
    project_info = get_project_info(project_data=project_data)
    keyboard = get_buy_projects_keyboard(
        project_list=project_list,
        theme_id=theme_id,
        price_from=price_from,
        price_up_to=price_up_to,
        page=page,
        status=status
    )
    await query.message.edit_text(text=project_info, reply_markup=keyboard)
    await bot.answer_callback_query(query.id)


async def search_by_theme_callback(query: CallbackQuery, callback_data: dict):
    price_from = callback_data.get("price_from")
    price_up_to = callback_data.get("price_up_to")
    await query.message.answer(
        text=MESSAGES["themes_list"],
        reply_markup=chose_themes_keyboard(
            price_from=price_from,
            price_up_to=price_up_to
        )
    )


async def search_by_price_callback(query: CallbackQuery, callback_data: dict, state: FSMContext):
    theme_id = callback_data.get("theme_id")
    await query.message.answer(
        text=MESSAGES["chose_price_from"], reply_markup=buy_menu()
    )
    await state.update_data(theme_id=theme_id)
    await state.set_state(BuyProjectStates.price_from)


def register_buy_handlers(dp: Dispatcher):
    dp.register_message_handler(get_main_keyboard, text=BUTTONS["back"])
    dp.register_message_handler(search_project_by_button, text=[BUTTONS["buy_menu"]])
    dp.register_message_handler(
        search_project_by_command, commands=[COMMANDS["search_project"]]
    )
    dp.register_message_handler(price_from_state, state=BuyProjectStates.price_from)
    dp.register_message_handler(price_up_to_state, state=BuyProjectStates.price_up_to)
    dp.register_callback_query_handler(
        buy_project_index_by_callback, themes_callback.filter()
    )
    dp.register_callback_query_handler(
        buy_project_page_handler, buy_project_callback.filter()
    )
    dp.register_callback_query_handler(chose_params_callback, chose_search_params_callback.filter())
    dp.register_callback_query_handler(search_by_theme_callback, search_by_theme_params_callback.filter())
    dp.register_callback_query_handler(search_by_price_callback, search_by_price_params_callback.filter())