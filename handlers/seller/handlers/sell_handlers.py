from datetime import datetime, timedelta

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
from data_base.db_functions import (
    get_moderator_id,
    get_need_payment,
    get_regular_sell_price,
    get_vip_sell_price,
)
from data_base.project import Project
from handlers.main_handlers import get_main_keyboard
from handlers.seller.inner_functions.seller_keyboard_markups import (
    get_back_menu_keyboard,
    get_cancel_menu_keyboard,
    get_main_sell_keyboard,
    get_project_confirmation_menu_keyboard,
)
from states import SellProjectStates
from texts.buttons import BUTTONS
from texts.messages import MESSAGES
from useful.instruments import bot, db_manager

projects_in_moderation = list()
moderation_dict = {}
new_projects_dict = {}
moderators_confirm_callback = CallbackData(
    "moderator_confirm", "project_data_id", "user_id"
)
moderators_reject_callback = CallbackData(
    "moderator_reject", "project_data_id", "user_id"
)


async def show_main_sell_keyboard(message: Message):
    await message.answer(
        text=MESSAGES["sell_menu"].format(message.from_user),
        reply_markup=get_main_sell_keyboard(),
    )


async def put_up_for_sale(message: Message):
    if message.from_user.username is not None:
        if message.chat.id in projects_in_moderation:
            await bot.send_message(
                chat_id=message.chat.id,
                text=MESSAGES["already_in_moderation"],
                reply_markup=get_main_sell_keyboard(),
            )
        else:
            await message.answer(text=MESSAGES["put_up_for_sale"])
            await message.answer(
                text=MESSAGES["project_name"], reply_markup=get_back_menu_keyboard()
            )
            await SellProjectStates.project_name.set()
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["empty_username"],
            reply_markup=get_main_sell_keyboard(),
        )


async def project_name_state(message: Message, state: FSMContext):
    await state.update_data(seller=message.from_user.username)
    answer = message.text
    if answer == BUTTONS["back_to_sell_menu"]:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["sell_menu"],
            reply_markup=get_main_sell_keyboard(),
        )
        await state.finish()
    else:
        if len(answer) < 50:
            await state.update_data(project_name=answer)
            await message.answer(
                MESSAGES["link"], reply_markup=get_cancel_menu_keyboard()
            )
            await SellProjectStates.link.set()
        else:
            await message.answer(
                text=MESSAGES["name_so_big"], reply_markup=get_back_menu_keyboard()
            )
            await SellProjectStates.project_name.set()


async def link_state(message: Message, state: FSMContext):
    answer = message.text
    if answer == BUTTONS["cancel"]:
        await message.answer(
            MESSAGES["project_name"], reply_markup=get_back_menu_keyboard()
        )
        await SellProjectStates.project_name.set()
    elif answer == BUTTONS["back_to_sell_menu"]:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["sell_menu"],
            reply_markup=get_main_sell_keyboard(),
        )
        await state.finish()
    else:
        await state.update_data(link=answer)
        await message.answer(MESSAGES["price"], reply_markup=get_cancel_menu_keyboard())
        await SellProjectStates.price.set()


async def price_state(message: Message, state: FSMContext):
    answer = message.text
    if answer == BUTTONS["cancel"]:
        await message.answer(MESSAGES["link"], reply_markup=get_back_menu_keyboard())
        await SellProjectStates.link.set()
    elif answer == BUTTONS["back_to_sell_menu"]:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["sell_menu"],
            reply_markup=get_main_sell_keyboard(),
        )
        await state.finish()
    else:
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["price_check"], reply_markup=ReplyKeyboardRemove()
            )
            await SellProjectStates.price.set()
        else:
            await state.update_data(price=answer)
            await message.answer(
                text=MESSAGES["subscribers"], reply_markup=get_cancel_menu_keyboard()
            )
            await SellProjectStates.subscribers.set()


async def subscribers_state(message: Message, state: FSMContext):
    answer = message.text
    if answer == BUTTONS["cancel"]:
        await message.answer(MESSAGES["price"], reply_markup=get_cancel_menu_keyboard())
        await SellProjectStates.price.set()
    elif answer == BUTTONS["back_to_sell_menu"]:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["sell_menu"],
            reply_markup=get_main_sell_keyboard(),
        )
        await state.finish()
    else:
        if not answer.isdigit():
            await message.answer(text=MESSAGES["subscribers_check"])
            await SellProjectStates.subscribers.set()

        else:
            if int(answer) < 1000000000:
                await state.update_data(subscribers=answer)
                await state.update_data(themes=[])
                await message.answer(
                    text=MESSAGES["themes"], reply_markup=themes_menu()
                )
                await SellProjectStates.themes_names.set()
            else:
                await message.answer(
                    text=MESSAGES["to_many_subscribers"],
                    reply_markup=get_cancel_menu_keyboard(),
                )
                await SellProjectStates.subscribers.set()


async def themes_names_state(message: Message, state: FSMContext):
    themes_dict = db_manager.get_all_themes()
    themes_list = themes_dict.values()
    message_text = message.text
    if message_text == BUTTONS["cancel"]:
        await message.answer(
            MESSAGES["subscribers"], reply_markup=get_cancel_menu_keyboard()
        )
        await SellProjectStates.subscribers.set()
    elif message_text == BUTTONS["back_to_sell_menu"]:
        await bot.send_message(
            text=MESSAGES["sell_menu"],
            reply_markup=get_main_sell_keyboard(),
        )
        await state.finish()
    else:
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
                    text=MESSAGES["themes_warn_2"], reply_markup=yes_or_no_keyboard()
                )
                await SellProjectStates.themes_plus.set()
            await state.update_data(themes=answer)
            size = len(answer)
            if size < 3:
                await message.answer(
                    text=MESSAGES["themes_plus"], reply_markup=yes_or_no_keyboard()
                )
                await SellProjectStates.themes_plus.set()
            else:
                await message.answer(
                    text=MESSAGES["income"], reply_markup=get_cancel_menu_keyboard()
                )
                await SellProjectStates.income.set()
        else:

            await message.answer(
                text=MESSAGES["themes_warn"], reply_markup=themes_menu()
            )
            await SellProjectStates.themes_names.set()


def themes_menu():
    themes_dict = db_manager.get_all_themes()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(KeyboardButton(BUTTONS["cancel"]))
    for key in themes_dict:
        markup.add(KeyboardButton(themes_dict[key]))
    return markup


async def themes_plus_state(message: Message):
    answer = message.text
    if answer == BUTTONS["yes"]:
        await message.answer(text=MESSAGES["themes_plus_1"], reply_markup=themes_menu())
        await SellProjectStates.themes_names.set()
    elif answer == BUTTONS["no"]:
        await message.answer(
            text=MESSAGES["income"], reply_markup=get_cancel_menu_keyboard()
        )
        await SellProjectStates.income.set()
    else:
        await message.answer(
            text=MESSAGES["yes_or_no"], reply_markup=yes_or_no_keyboard()
        )
        await SellProjectStates.themes_plus.set()


def yes_or_no_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    yes_button = KeyboardButton(BUTTONS["yes"])
    no_button = KeyboardButton(BUTTONS["no"])
    markup.add(yes_button, no_button)
    return markup


async def income_state(message: Message, state: FSMContext):
    answer = message.text
    if answer == BUTTONS["cancel"]:
        await state.update_data(themes=[])
        await message.answer(MESSAGES["themes"], reply_markup=themes_menu())
        await SellProjectStates.themes_names.set()
    elif answer == BUTTONS["back_to_sell_menu"]:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["sell_menu"],
            reply_markup=get_main_sell_keyboard(),
        )
        await state.finish()
    else:
        if not answer.isdigit():
            await message.answer(
                text=MESSAGES["income_check"], reply_markup=get_cancel_menu_keyboard()
            )
            await SellProjectStates.income.set()
        else:
            await state.update_data(income=answer)
            await message.answer(
                text=MESSAGES["comment"], reply_markup=get_cancel_menu_keyboard()
            )
            await SellProjectStates.comment.set()


async def comment_state(message: Message, state: FSMContext):
    answer = message.text
    if answer == BUTTONS["cancel"]:
        await state.update_data(themes=[])
        await message.answer(
            MESSAGES["income"], reply_markup=get_cancel_menu_keyboard()
        )
        await SellProjectStates.income.set()
    elif answer == BUTTONS["back_to_sell_menu"]:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["sell_menu"],
            reply_markup=get_main_sell_keyboard(),
        )
        await state.finish()
    else:
        if len(answer) < 1000:
            await state.update_data(comment=answer)
            await message.answer(
                text=MESSAGES["status"], reply_markup=yes_or_no_keyboard()
            )
            await SellProjectStates.status.set()
        else:
            await message.answer(
                text=MESSAGES["comment_so_big"], reply_markup=get_cancel_menu_keyboard()
            )
            await SellProjectStates.comment.set()


async def status_state(message: Message, state: FSMContext):
    answer = message.text
    if answer == BUTTONS["cancel"]:
        await message.answer(
            MESSAGES["comment"], reply_markup=get_cancel_menu_keyboard()
        )
        await SellProjectStates.comment.set()
    elif answer == BUTTONS["back_to_sell_menu"]:
        await bot.send_message(
            text=MESSAGES["sell_menu"],
            reply_markup=get_main_sell_keyboard(),
        )
        await state.finish()
    else:
        if answer == BUTTONS["yes"]:
            await state.update_data(status=1)
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
                seller=message.from_user.username + " 🌟",
                price=data["price"],
                link=data["link"],
            )
            await message.answer(
                text=project_info, reply_markup=get_project_confirmation_menu_keyboard()
            )
            await SellProjectStates.confirm.set()
        elif answer == BUTTONS["no"]:
            await state.update_data(status=0)
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
                link=data["link"],
            )
            await message.answer(
                text=project_info, reply_markup=get_project_confirmation_menu_keyboard()
            )
            await SellProjectStates.confirm.set()
        else:
            await message.answer(
                text=MESSAGES["yes_or_no"], reply_markup=yes_or_no_keyboard()
            )
            await SellProjectStates.status.set()


async def moderators_confirm_state(message: Message, state: FSMContext):
    answer = message.text
    if answer == BUTTONS["cancel"]:
        await message.answer(MESSAGES["status"], reply_markup=yes_or_no_keyboard())
        await SellProjectStates.status.set()
    elif answer == BUTTONS["back_to_sell_menu"]:
        await bot.send_message(
            text=MESSAGES["sell_menu"],
            reply_markup=get_main_sell_keyboard(),
        )
        await state.finish()
    else:
        await state.update_data(buy_process=answer)
        if answer == BUTTONS["confirm"]:
            await bot.send_message(
                message.chat.id,
                text=MESSAGES["moderation"],
                reply_markup=get_main_keyboard(),
            )
            data = await state.get_data()
            themes_str = ""
            for i in data["themes"]:
                themes_str += "#" + str(i) + " "
            project_info = MESSAGES["moderator_confirm"].format(
                name=data["project_name"],
                themes=themes_str,
                subs=data["subscribers"],
                income=data["income"],
                comm=data["comment"],
                seller=message.from_user.username,
                price=data["price"],
                link=data["link"],
            )
            dict_id = str(message.chat.id)
            moderation_dict[dict_id] = data
            projects_in_moderation.append(message.chat.id)
            keyboard = InlineKeyboardMarkup(row_width=1)
            reject_button = InlineKeyboardButton(
                text=BUTTONS["reject"],
                callback_data=moderators_reject_callback.new(
                    project_data_id=dict_id, user_id=message.chat.id
                ),
            )
            confirm_button = InlineKeyboardButton(
                text=BUTTONS["confirm"],
                callback_data=moderators_confirm_callback.new(
                    project_data_id=dict_id, user_id=message.chat.id
                ),
            )
            keyboard.add(confirm_button)
            keyboard.add(reject_button)
            await bot.send_message(
                chat_id=get_moderator_id(), text=project_info, reply_markup=keyboard
            )
        elif answer == BUTTONS["cancellation"]:
            is_moderator = False
            if message.chat.id == get_moderator_id():
                is_moderator = True
            await bot.send_message(
                message.chat.id,
                MESSAGES["main_menu"].format(message.from_user),
                reply_markup=get_main_keyboard(is_moderator=is_moderator),
            )

        await state.finish()


async def moderators_confirm(query: CallbackQuery, callback_data: dict):
    await query.message.delete()
    user_id = int(callback_data.get("user_id"))
    data_id = callback_data.get("project_data_id")
    data = moderation_dict[data_id]
    moderation_dict.pop(data_id)
    new_project = Project()
    new_project.name = data["project_name"]
    new_project.seller_name = data["seller"]
    new_project.status_id = data["status"]
    new_project.price = data["price"]
    new_project.subscribers = data["subscribers"]
    new_project.themes_names = data["themes"]
    new_project.income = data["income"]
    new_project.comment = data["comment"]
    new_project.link = data["link"]
    need_payment = get_need_payment()
    projects_in_moderation.remove(user_id)
    if need_payment == 1:
        price_amount = 0
        if new_project.status_id == 0:
            price_amount = get_regular_sell_price()
        elif new_project.status_id == 1:
            price_amount = get_vip_sell_price()
        prices = [LabeledPrice(label=MESSAGES["sell_payment"], amount=price_amount)]
        new_projects_dict[new_project.seller_name] = new_project
        await bot.send_invoice(
            user_id,
            title=MESSAGES["sell_payment_title"],
            description=MESSAGES["sell_payment_description"],
            provider_token=PAYMENTS_TOKEN,
            currency="rub",
            is_flexible=False,
            prices=prices,
            start_parameter="example",
            payload="some_invoice",
        )
    elif need_payment == 0:
        new_project.save_new_project()
        is_moderator = False
        if user_id == get_moderator_id():
            is_moderator = True
        await bot.send_message(
            user_id,
            MESSAGES["save_project"],
            reply_markup=get_main_keyboard(is_moderator=is_moderator),
        )


async def moderators_reject(query: CallbackQuery, callback_data: dict):
    await query.message.delete()
    user_id = int(callback_data.get("user_id"))
    data_id = callback_data.get("project_data_id")
    data = moderation_dict[data_id]
    moderation_dict.pop(data_id)
    new_project = Project()
    new_project.name = data["project_name"]
    new_project.seller_name = data["seller"]
    new_project.status_id = 0
    new_project.price = data["price"]
    new_project.subscribers = data["subscribers"]
    new_project.themes_names = data["themes"]
    new_project.income = data["income"]
    new_project.comment = data["comment"]
    projects_in_moderation.remove(user_id)
    is_moderator = False
    if user_id == get_moderator_id():
        is_moderator = True
    await bot.send_message(
        user_id,
        MESSAGES["rejected_project"] % new_project.name,
        reply_markup=get_main_keyboard(is_moderator=is_moderator),
    )


async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def successful_payment(message: Message):

    if new_projects_dict[message.from_user.username].status_id == 1:
        new_projects_dict[
            message.from_user.username
        ].vip_ending = datetime.now() + timedelta(days=7)
    else:
        new_projects_dict[
            message.from_user.username
        ].vip_ending = datetime(year=1900, month=1, day=1)

    new_projects_dict[message.from_user.username].save_new_project()
    new_projects_dict.pop(message.from_user.username)
    is_moderator = False
    if message.chat.id == get_moderator_id():
        is_moderator = True
    await bot.send_message(
        message.chat.id,
        MESSAGES["successful_payment"].format(
            total_amount=message.successful_payment.total_amount // 100,
            currency=message.successful_payment.currency,
        ),
        reply_markup=get_main_keyboard(is_moderator=is_moderator),
    )


def register_sell_handlers(dp: Dispatcher):
    dp.register_message_handler(show_main_sell_keyboard, text=[BUTTONS["sell_menu"]])
    dp.register_message_handler(put_up_for_sale, text=[BUTTONS["sell_project"]])
    dp.register_message_handler(
        project_name_state, state=SellProjectStates.project_name
    )
    dp.register_message_handler(link_state, state=SellProjectStates.link)
    dp.register_message_handler(price_state, state=SellProjectStates.price)
    dp.register_message_handler(subscribers_state, state=SellProjectStates.subscribers)
    dp.register_message_handler(
        themes_names_state, state=SellProjectStates.themes_names
    )
    dp.register_message_handler(themes_plus_state, state=SellProjectStates.themes_plus)
    dp.register_message_handler(income_state, state=SellProjectStates.income)
    dp.register_message_handler(comment_state, state=SellProjectStates.comment)
    dp.register_message_handler(status_state, state=SellProjectStates.status)
    dp.register_message_handler(
        moderators_confirm_state, state=SellProjectStates.confirm
    )
    dp.register_pre_checkout_query_handler(checkout_process, lambda q: True)
    dp.register_message_handler(
        successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT
    )
    dp.register_callback_query_handler(
        moderators_confirm, moderators_confirm_callback.filter()
    )
    dp.register_callback_query_handler(
        moderators_reject, moderators_reject_callback.filter()
    )
