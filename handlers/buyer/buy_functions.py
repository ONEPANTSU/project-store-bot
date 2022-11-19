from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from data_base.db_functions import get_guarantee_name, get_project_list_by_filter
from handlers.buyer.buy_callbacks import buy_project_callback, themes_callback, chose_search_params_callback, \
    search_by_price_params_callback, search_by_theme_params_callback
from texts.buttons import BUTTONS
from texts.messages import MESSAGES
from useful.instruments import bot, db_manager


async def show_all_projects(message: Message):
    await message.answer(text=MESSAGES["buy_menu"])
    await buy_project_index(
        chat_id=message.chat.id, theme_id="None", price_from="None", price_up_to="None"
    )


def buy_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    back_button = KeyboardButton(BUTTONS["back"])
    markup.add(back_button)
    return markup


async def buy_project_index(chat_id, theme_id, price_from, price_up_to, status: int = 0):
    project_list = get_project_list_by_filter(
        theme_id=theme_id, price_from=price_from, price_up_to=price_up_to
    )
    if len(project_list) != 0:
        project_data = project_list[0]
        project_info = get_project_info(project_data=project_data)
        keyboard = get_buy_projects_keyboard(
            project_list=project_list,
            theme_id=theme_id,
            price_from=price_from,
            price_up_to=price_up_to,
            status=status,
        )
        await bot.send_message(
            chat_id=chat_id,
            text=project_info,
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    else:
        await bot.send_message(chat_id=chat_id, text=MESSAGES["list_is_empty"])


def chose_themes_keyboard(price_from="None", price_up_to="None"):
    # С помощью функции get_all_themes() присваиваем в themes - словарь с темами и их айди
    themes = db_manager.get_filled_themes()
    themes_keyboard = InlineKeyboardMarkup(row_width=2)
    # Заполнение списка тем из словаря с базы данных
    for theme_key in themes.keys():
        themes_keyboard.add(
            InlineKeyboardButton(
                text=themes[theme_key],
                callback_data=themes_callback.new(
                    theme_id="{}".format(theme_key),
                    price_from=price_from,
                    price_up_to=price_up_to,
                ),
            )
        )
    return themes_keyboard


# Клавиатура для карусели по листу проектов
def get_buy_projects_keyboard(
    project_list, theme_id, price_from, price_up_to, status, page: int = 0
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    has_next_page = len(project_list) > page + 1

    page_num_button = InlineKeyboardButton(
        text=f"{page + 1} / {len(project_list)}", callback_data="dont_click_me"
    )

    keyboard.row(page_num_button)

    if status == 0:
        params_button = InlineKeyboardButton(
            text=BUTTONS["chose_search_params"],
            callback_data=chose_search_params_callback.new(
                page=page,
                theme_id=theme_id,
                price_from=price_from,
                price_up_to=price_up_to,
            )
        )
        keyboard.row(params_button)

    elif status == 1:
        price_button = InlineKeyboardButton(
            text="Цена ₽",
            callback_data=search_by_price_params_callback.new(
                theme_id=theme_id
            )
        )
        theme_button = InlineKeyboardButton(
            text="Тематика #",
            callback_data=search_by_theme_params_callback.new(
                price_from=price_from,
                price_up_to=price_up_to
            )
        )
        keyboard.row(price_button, theme_button)

    back_button = InlineKeyboardButton(
        text=BUTTONS["prev"],
        callback_data=buy_project_callback.new(
            page=page - 1,
            theme_id=theme_id,
            price_from=price_from,
            price_up_to=price_up_to,
            status=status
        ),
    )

    next_button = InlineKeyboardButton(
        text=BUTTONS["next"],
        callback_data=buy_project_callback.new(
            page=page + 1,
            theme_id=theme_id,
            price_from=price_from,
            price_up_to=price_up_to,
            status=status
        ),
    )

    if page != 0:
        if has_next_page:
            keyboard.row(back_button, next_button)
        else:
            keyboard.row(back_button)
    elif has_next_page:
        keyboard.row(next_button)

    return keyboard


def get_project_info(project_data):  # Page: 0
    guarantee = get_guarantee_name()
    themes_str = ""
    for theme_name in project_data.themes_names:
        themes_str += "#" + str(theme_name) + " "

    if project_data.is_verified == 1:
        data_verified = MESSAGES["verified"]

        project_info = MESSAGES["show_verified_project"].format(
            link=project_data.link,
            verified=data_verified,
            name=project_data.name,
            themes=themes_str,
            subs=project_data.subscribers,
            income=project_data.income,
            comm=project_data.comment,
            seller=project_data.seller_name,
            price=project_data.price,
            guarantee=guarantee,
        )
    else:
        project_info = MESSAGES["show_not_verified_project"].format(
            link=project_data.link,
            name=project_data.name,
            themes=themes_str,
            subs=project_data.subscribers,
            income=project_data.income,
            comm=project_data.comment,
            seller=project_data.seller_name,
            price=project_data.price,
            guarantee=guarantee,
        )

    return project_info
