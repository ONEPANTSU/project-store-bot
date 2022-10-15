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
from data_base.db_functions import get_need_payment, get_to_sell_price
from data_base.project import Project
from handlers.main_handlers import get_main_keyboard
from handlers.seller.seller_keyboard_markups import (
    get_back_menu_keyboard,
    get_cancel_menu_keyboard,
    get_main_sell_keyboard,
    get_project_confirmation_menu_keyboard,
)
from instruments import bot, db_manager
from states import SellProjectStates
from texts.buttons import BUTTONS
from texts.messages import MESSAGES

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
                MESSAGES["price"], reply_markup=get_cancel_menu_keyboard()
            )
            await SellProjectStates.price.set()
        else:
            await message.answer(
                text=MESSAGES["name_so_big"], reply_markup=get_back_menu_keyboard()
            )
            await SellProjectStates.project_name.set()


async def price_state(message: Message, state: FSMContext):
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
            text=MESSAGES["yes_or_no"], reply_markup=themes_plus_keyboard()
        )
        await SellProjectStates.themes_plus.set()


def themes_plus_keyboard():
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
        await message.answer(
            MESSAGES["income"], reply_markup=get_cancel_menu_keyboard()
        )
        await SellProjectStates.income.set()
    elif answer == BUTTONS["back_to_sell_menu"]:
        await bot.send_message(
            text=MESSAGES["sell_menu"],
            reply_markup=get_main_sell_keyboard(),
        )
        await state.finish()
    else:
        if len(answer) < 1000:
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
            await message.answer(
                text=project_info, reply_markup=get_project_confirmation_menu_keyboard()
            )
            await SellProjectStates.confirm.set()
        else:
            await message.answer(
                text=MESSAGES["comment_so_big"], reply_markup=get_cancel_menu_keyboard()
            )
            await SellProjectStates.comment.set()


async def moderators_confirm_state(message: Message, state: FSMContext):
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
        await state.update_data(buy_process=answer)
        if answer == BUTTONS["confirm"]:
            await bot.send_message(
                message.chat.id,
                text=MESSAGES["moderation"],
                reply_markup=get_main_keyboard(),
            )
            data = await state.get_data()
            await state.finish()
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
            )
            dict_id = str(message.chat.id) + " " + data["project_name"]
            moderation_dict[dict_id] = data
            moderators = db_manager.get_moderators_names()
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
            for moderator in moderators:
                moderator_id = moderator[0]
                await bot.send_message(
                    chat_id=moderator_id, text=project_info, reply_markup=keyboard
                )
        elif answer == BUTTONS["cancellation"]:
            await state.finish()
            await bot.send_message(
                chat_id=message.chat.id,
                text=MESSAGES["main_menu"].format(message.from_user),
                reply_markup=get_main_keyboard(),
            )


async def moderators_confirm(query: CallbackQuery, callback_data: dict):
    await query.message.delete()
    user_id = callback_data.get("user_id")
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
    need_payment = get_need_payment()
    if need_payment == 1:
        price_amount = get_to_sell_price()
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
        await bot.send_message(
            user_id,
            MESSAGES["save_project"],
            reply_markup=ReplyKeyboardRemove(),
        )


async def moderators_reject(query: CallbackQuery, callback_data: dict):
    await query.message.delete()
    user_id = callback_data.get("user_id")
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
    await bot.send_message(
        user_id,
        MESSAGES["rejected_project"] % new_project.name,
        reply_markup=ReplyKeyboardRemove(),
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
        ),
        reply_markup=get_main_sell_keyboard(),
    )


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
