from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    CallbackQuery,
    ContentType,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.utils.callback_data import CallbackData

from config import PAYMENTS_TOKEN
from data_base.project import (
    Project,
    get_guarantee_name,
    get_need_payment,
    get_projects_list_by_seller_name,
    get_to_sell_price,
)
from handlers.main_handlers import get_main_keyboard
from instruments import bot, db_manager
from states import SellProjectStates
from texts.buttons import BUTTONS
from texts.messages import MESSAGES

new_projects_dict = {}
my_projects_callback = CallbackData("my_projects", "page")
delete_project_callback = CallbackData("delete_project", "id", "page")


async def show_main_sell_keyboard(message: Message):
    await message.answer(
        text=MESSAGES["sell_menu"].format(message.from_user),
        reply_markup=get_main_sell_keyboard(),
    )


def get_main_sell_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    to_sell_project_button = KeyboardButton(BUTTONS["sell_project"])
    list_of_my_projects_button = KeyboardButton(BUTTONS["sell_list"])
    back_button = KeyboardButton(BUTTONS["back"])
    markup.add(to_sell_project_button, list_of_my_projects_button, back_button)
    return markup


async def put_up_for_sale(message: Message):
    await message.answer(
        text=MESSAGES["put_up_for_sale"].format(message.from_user),
        reply_markup=get_main_keyboard(),
    )
    await message.answer(
        text=MESSAGES["project_name"], reply_markup=ReplyKeyboardRemove()
    )
    await SellProjectStates.project_name.set()


async def project_name_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(project_name=answer)
    await message.answer(MESSAGES["price"])
    await SellProjectStates.price.set()


async def price_state(message: Message, state: FSMContext):
    answer = message.text
    if not answer.isdigit():
        await message.answer(text=MESSAGES["price_check"])
        await SellProjectStates.price.set()
    else:
        await state.update_data(price=answer)
        await message.answer(text=MESSAGES["subscribers"])
        await SellProjectStates.subscribers.set()


async def subscribers_state(message: Message, state: FSMContext):
    answer = message.text
    if not answer.isdigit():
        await message.answer(text=MESSAGES["subscribers_check"])
        await SellProjectStates.subscribers.set()
    else:
        await state.update_data(subscribers=answer)
        await message.answer(text=MESSAGES["themes"], reply_markup=themes_menu())
        await SellProjectStates.themes_names.set()


async def themes_names_state(message: Message, state: FSMContext):
    themes_dict = db_manager.get_all_themes()
    themes_list = themes_dict.values()
    message_text = message.text
    if message_text in themes_list:
        answer = list()
        data = await state.get_data()
        themes = data.get("themes", False)
        if themes:
            answer = data["themes"]
        if message.text not in answer:
            answer.append(message.text)
        else:
            await message.answer(
                text=MESSAGES["themes_warn_2"], reply_markup=themes_plus_keyboard()
            )
            await SellProjectStates.themes_plus.set()
        await state.update_data(themes=answer)
        size = len(answer)
        if size < 3:
            await message.answer(
                text=MESSAGES["themes_plus"], reply_markup=themes_plus_keyboard()
            )
            await SellProjectStates.themes_plus.set()
        else:
            await message.answer(text=MESSAGES["income"], reply_markup=ReplyKeyboardRemove())
            await SellProjectStates.income.set()
    else:

        await message.answer(text=MESSAGES["themes_warn"], reply_markup=themes_menu())
        await SellProjectStates.themes_names.set()


def themes_menu():
    themes_dict = db_manager.get_all_themes()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for key in themes_dict:
        markup.add(KeyboardButton(themes_dict[key]))
    return markup


async def themes_plus_state(message: Message):
    answer = message.text
    if answer == "Да":
        await message.answer(text=MESSAGES["themes_plus_1"], reply_markup=themes_menu())
        await SellProjectStates.themes_names.set()
    elif answer == "Нет":
        await message.answer(text=MESSAGES["income"], reply_markup=ReplyKeyboardRemove())
        await SellProjectStates.income.set()


def themes_plus_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    yes_button = KeyboardButton(BUTTONS["yes"])
    no_button = KeyboardButton(BUTTONS["no"])
    markup.add(yes_button, no_button)
    return markup


async def income_state(message: Message, state: FSMContext):
    answer = message.text
    if not answer.isdigit():
        await message.answer(text=MESSAGES["income_check"])
        await SellProjectStates.income.set()
    else:
        await state.update_data(income=answer)
        await message.answer(text=MESSAGES["comment"])
        await SellProjectStates.comment.set()


async def comment_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(comment=answer)
    data = await state.get_data()
    themes_str = ""
    for i in data["themes"]:
        themes_str += "#" + str(i) + " "
    project_info = MESSAGES["confirm"].format(
        name=data["project_name"],
        themes=themes_str,
        subs=data["subscribers"],
        income=data["income"],
        comm=data["comment"],
        seller=message.from_user.username,
        price=data["price"],
    )
    await message.answer(text=project_info, reply_markup=project_confirmation_menu())
    await SellProjectStates.buy_process.set()


def project_confirmation_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    confirm_button = KeyboardButton(BUTTONS["confirm"])
    cancellation_button = KeyboardButton(BUTTONS["cancellation"])
    markup.add(confirm_button, cancellation_button)
    return markup


async def buy_process(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(buy_process=answer)
    if answer == BUTTONS["confirm"]:
        data = await state.get_data()
        new_project = Project()
        new_project.name = data["project_name"]
        new_project.seller_name = message.from_user.username
        new_project.status_id = 0
        new_project.price = data["price"]
        new_project.subscribers = data["subscribers"]
        new_project.themes_names = data["themes"]
        new_project.income = data["income"]
        new_project.comment = data["comment"]
        need_payment = get_need_payment()
        if need_payment == 1:
            price_amount = get_to_sell_price()
            prices = [LabeledPrice(label=MESSAGES["sell_payment"], amount=price_amount)]
            new_projects_dict[message.from_user.username] = new_project
            await bot.send_invoice(
                message.chat.id,
                title=MESSAGES["sell_payment_title"],
                description=MESSAGES["sell_payment_description"],
                provider_token=PAYMENTS_TOKEN,
                currency="rub",
                is_flexible=False,
                prices=prices,
                start_parameter="example",
                payload="some_invoice",
            )
            await state.finish()
        elif need_payment == 0:
            new_project.save_new_project()
            await bot.send_message(
                message.chat.id,
                MESSAGES["save_project"], reply_markup=ReplyKeyboardRemove()
            )
    elif answer == BUTTONS["cancellation"]:
        await state.finish()
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["main_menu"].format(message.from_user),
            reply_markup=get_main_keyboard(),
        )


async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def successful_payment(message: Message):
    new_projects_dict[message.from_user.username].save_new_project()
    new_projects_dict.pop(message.from_user.username)
    await bot.send_message(
        message.chat.id,
        MESSAGES["successful_payment"].format(
            total_amount=message.successful_payment.total_amount // 100,
            currency=message.successful_payment.currency,
        ), reply_markup=ReplyKeyboardRemove()
    )


def get_my_projects_keyboard(project_list, page: int = 0) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    has_next_page = len(project_list) > page + 1

    page_num_button = InlineKeyboardButton(
        text=f"{page + 1} / {len(project_list)}", callback_data="dont_click_me"
    )

    delete_button = InlineKeyboardButton(
        text=BUTTONS["delete_project"], callback_data=delete_project_callback.new(id=project_list[page].id, page=0)
    )

    back_button = InlineKeyboardButton(
        text=BUTTONS["prev"], callback_data=my_projects_callback.new(page=page - 1)
    )

    next_button = InlineKeyboardButton(
        text=BUTTONS["next"], callback_data=my_projects_callback.new(page=page + 1)
    )

    keyboard.row(page_num_button)
    keyboard.row(delete_button)
    if page != 0:
        if has_next_page:
            keyboard.row(back_button, next_button)
        else:
            keyboard.row(back_button)
    elif has_next_page:
        keyboard.row(next_button)

    return keyboard


async def my_project_index(message: Message):
    project_list = get_projects_list_by_seller_name(message.from_user.username)
    if len(project_list) != 0:
        project_data = project_list[0]
        keyboard = get_my_projects_keyboard(project_list=project_list)  # Page: 0
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
        await bot.send_message(
            chat_id=message.chat.id,
            text=project_info,
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["empty_projects"]
        )


async def my_project_page_handler(query: CallbackQuery, callback_data: dict):
    await refresh_pages(query=query, callback_data=callback_data)


async def delete_project_handler(query: CallbackQuery, callback_data: dict):
    db_manager.delete_project(int(callback_data.get("id")))
    await bot.send_message(chat_id=query.message.chat.id, text=MESSAGES["deleted_project"])
    await refresh_pages(query=query, callback_data=callback_data)


async def refresh_pages(query: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))

    project_list = get_projects_list_by_seller_name(query.from_user.username)
    if len(project_list) != 0:
        project_data = project_list[page]
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
        keyboard = get_my_projects_keyboard(project_list=project_list, page=page)

        await query.message.edit_text(text=project_info, reply_markup=keyboard)
    else:
        await query.message.edit_text(text=MESSAGES["empty_projects"], reply_markup=None)


def back_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    back_button = KeyboardButton(BUTTONS["back"])
    markup.add(back_button)
    return markup


def register_sell_handlers(dp: Dispatcher):
    dp.register_message_handler(show_main_sell_keyboard, text=[BUTTONS["sell_menu"]])
    dp.register_message_handler(put_up_for_sale, text=[BUTTONS["sell_project"]])
    dp.register_message_handler(
        project_name_state, state=SellProjectStates.project_name
    )
    dp.register_message_handler(price_state, state=SellProjectStates.price)
    dp.register_message_handler(subscribers_state, state=SellProjectStates.subscribers)
    dp.register_message_handler(
        themes_names_state, state=SellProjectStates.themes_names
    )
    dp.register_message_handler(themes_plus_state, state=SellProjectStates.themes_plus)
    dp.register_message_handler(income_state, state=SellProjectStates.income)
    dp.register_message_handler(comment_state, state=SellProjectStates.comment)
    dp.register_message_handler(buy_process, state=SellProjectStates.buy_process)
    dp.register_pre_checkout_query_handler(checkout_process, lambda q: True)
    dp.register_message_handler(
        successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT
    )
    dp.register_message_handler(my_project_index, text=BUTTONS["sell_list"])
    dp.register_callback_query_handler(
        my_project_page_handler, my_projects_callback.filter()
    )
    dp.register_callback_query_handler(
        delete_project_handler, delete_project_callback.filter()
    )
