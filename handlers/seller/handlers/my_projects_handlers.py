from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, LabeledPrice, Message, ReplyKeyboardRemove

from config import PAYMENTS_TOKEN
from data_base.db_functions import get_moderator_id, get_vip_sell_price
from data_base.discount import Discount
from data_base.project import Project
from handlers.main.main_functions import get_main_keyboard
from handlers.seller.handlers.my_projects_functions import my_project_index_handler
from handlers.seller.handlers.sell_handlers import yes_or_no_keyboard
from handlers.seller.inner_functions.seller_carousel_pages import (
    get_delete_project_dict_info,
    refresh_pages,
)
from handlers.seller.inner_functions.seller_keyboard_markups import (
    get_back_menu_keyboard,
    get_main_sell_keyboard,
    get_project_confirmation_menu_keyboard,
)
from handlers.seller.instruments.seller_callbacks import (
    delete_project_callback,
    my_projects_callback,
    price_changing_callback,
    vip_project_callback,
)
from handlers.seller.instruments.seller_dicts import (
    delete_project_dict,
    is_moderator_dict,
    price_changing_project_dict,
    vip_project_dict,
)
from states import DeleteProjectStates, VipDiscountStates
from states.price_changing_states import PriceChangingStates
from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.invoice_payload import INVOICE_PAYLOAD
from texts.messages import MESSAGES
from useful.commands_handler import commands_handler
from useful.instruments import bot, db_manager


async def my_projects_by_button(message: Message):
    await my_project_index_handler(message)


async def my_projects_by_command(message: Message):
    await my_project_index_handler(message)


async def my_project_page_handler(query: CallbackQuery, callback_data: dict):
    await refresh_pages(query=query, callback_data=callback_data)


async def vip_project_handler(
    query: CallbackQuery, callback_data: dict, state: FSMContext
):
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=MESSAGES["vip_need_promo_code"],
        reply_markup=yes_or_no_keyboard(),
    )
    await state.update_data(project_id=callback_data.get("id"))
    await state.set_state(VipDiscountStates.is_need)


async def vip_need_promo_state(message: Message, state: FSMContext):
    answer = message.text
    if answer == BUTTONS["yes"]:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["input_promo_code"],
            reply_markup=ReplyKeyboardRemove(),
        )
        await VipDiscountStates.code.set()
    else:
        data = await state.get_data()
        project_id = data["project_id"]
        project = Project()
        project.set_params_by_id(project_id)
        price_amount = get_vip_sell_price()
        prices = [LabeledPrice(label=MESSAGES["sell_payment"], amount=price_amount)]
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["vip_payment_description"],
            reply_markup=get_main_sell_keyboard(),
        )
        await bot.send_invoice(
            message.chat.id,
            title=MESSAGES["sell_payment_title"],
            description=MESSAGES["vip_payment_description"],
            provider_token=PAYMENTS_TOKEN,
            currency="rub",
            is_flexible=False,
            prices=prices,
            start_parameter="example",
            payload=INVOICE_PAYLOAD["vip"],
        )
        await state.finish()
        if answer.lstrip("/") in COMMANDS.values():
            await commands_handler(message)


async def vip_input_promo_state(message: Message, state: FSMContext):
    data = await state.get_data()
    project_id = data["project_id"]
    project = Project()
    project.set_params_by_id(project_id)
    vip_project_dict[message.chat.username] = project
    price_amount = get_vip_sell_price()
    discounted_price = Discount().use_discount(message.text, price_amount)
    if discounted_price < price_amount:
        await state.finish()
        price_amount = discounted_price
        prices = [LabeledPrice(label=MESSAGES["sell_payment"], amount=price_amount)]
        await bot.send_invoice(
            message.chat.id,
            title=MESSAGES["sell_payment_title"],
            description=MESSAGES["sell_payment_description"],
            provider_token=PAYMENTS_TOKEN,
            currency="rub",
            is_flexible=False,
            prices=prices,
            start_parameter="example",
            payload=INVOICE_PAYLOAD["vip"],
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["wrong_promo_code"],
            reply_markup=yes_or_no_keyboard(),
        )
        await VipDiscountStates.is_need.set()


async def price_changing_handler(query: CallbackQuery, callback_data: dict):
    project = Project()
    project.set_params_by_id(callback_data.get("id"))
    price_changing_project_dict[query.message.chat.id] = project
    await query.message.answer(
        text=MESSAGES["change_price"], reply_markup=get_back_menu_keyboard()
    )
    await PriceChangingStates.price.set()


async def price_changing_state(message: Message, state: FSMContext):
    await state.update_data(seller=message.from_user.username)
    answer = message.text
    if answer.lstrip("/") in COMMANDS.values():
        await state.finish()
        await commands_handler(message)
    elif answer == BUTTONS["back_to_sell_menu"]:
        await my_project_index_handler(message)
        price_changing_project_dict.pop(message.chat.id)
        await state.finish()
    else:
        if not answer.isdigit():
            await message.answer(text=MESSAGES["price_check"])
            await PriceChangingStates.price.set()
        else:
            await state.update_data(price=answer)
            price_changing_project_dict[message.chat.id].price = answer
            await message.answer(
                text=MESSAGES["price_changing_confirm"],
                reply_markup=get_project_confirmation_menu_keyboard(back_button=False),
            )
            await PriceChangingStates.confirm.set()


async def price_changing_confirm_state(message: Message, state: FSMContext):
    answer = message.text
    if answer.lstrip("/") in COMMANDS.values():
        await state.finish()
        await commands_handler(message)
    elif answer == BUTTONS["cancellation"]:
        await my_project_index_handler(message)
        price_changing_project_dict.pop(message.chat.id)
        await state.finish()

    elif answer == BUTTONS["confirm"]:
        price_changing_project_dict[message.chat.id].save_changes_to_existing_project()
        is_moderator = False
        if message.from_user.id == get_moderator_id():
            is_moderator = True
        await bot.send_message(
            chat_id=message.chat.id,
            text=MESSAGES["price_changing_success"],
            reply_markup=get_main_keyboard(is_moderator),
        )
        await my_project_index_handler(message)
        price_changing_project_dict.pop(message.chat.id)
        await state.finish()

    else:
        await message.answer(
            text=MESSAGES["command_error"],
            reply_markup=get_project_confirmation_menu_keyboard(back_button=False),
        )
        await PriceChangingStates.confirm.set()


async def delete_project_handler(query: CallbackQuery, callback_data: dict):
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=MESSAGES["confirm_deleting"],
        reply_markup=get_project_confirmation_menu_keyboard(back_button=False),
    )
    is_moderator_str = callback_data.get("is_moderator")
    if is_moderator_str == "True":
        is_moderator = True
    else:
        is_moderator = False
    is_moderator_dict[query.message.chat.id] = is_moderator
    delete_project_dict[query.message.chat.id] = [
        int(callback_data.get("id")),
        query,
        callback_data,
    ]
    await DeleteProjectStates.confirm.set()


async def delete_confirm_handler(message: Message, state: FSMContext):
    answer = message.text
    if answer.lstrip("/") in COMMANDS.values():
        await state.finish()
        await commands_handler(message)
    else:
        await state.update_data(confitrm=answer)
        await check_delete_confirm(answer, message, state)


async def check_delete_confirm(answer, message, state):
    if answer == BUTTONS["confirm"]:
        await confirmed_deleting(message, state)
    elif answer == BUTTONS["cancellation"]:
        await canceled_deleting(message, state)
    else:
        await deleting_command_error(message)


async def deleting_command_error(message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=MESSAGES["command_error"],
        reply_markup=get_project_confirmation_menu_keyboard(),
    )
    await DeleteProjectStates.confirm.set()


async def canceled_deleting(message, state):
    if is_moderator_dict[message.chat.id]:
        reply_markup = get_main_keyboard(
            is_moderator=is_moderator_dict[message.chat.id]
        )
    else:
        reply_markup = get_main_sell_keyboard()
        await my_project_index_handler(message=message)
    is_moderator_dict.pop(message.chat.id)
    await bot.send_message(
        chat_id=message.chat.id,
        text=MESSAGES["not_deleted_project"],
        reply_markup=reply_markup,
    )
    delete_project_dict.pop(message.chat.id)
    await state.finish()


async def confirmed_deleting(message, state):
    callback_data, project_id, query = get_delete_project_dict_info(message.chat.id)
    db_manager.delete_project(project_id)
    if is_moderator_dict[message.chat.id]:
        reply_markup = get_main_keyboard(
            is_moderator=is_moderator_dict[message.chat.id]
        )
    else:
        reply_markup = get_main_sell_keyboard()
    is_moderator_dict.pop(message.chat.id)
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=MESSAGES["deleted_project"],
        reply_markup=reply_markup,
    )
    await refresh_pages(query=query, callback_data=callback_data)
    await state.finish()


def register_my_projects_handlers(dp: Dispatcher):
    dp.register_message_handler(my_projects_by_button, text=BUTTONS["sell_list"])
    dp.register_message_handler(
        my_projects_by_command, commands=COMMANDS["my_projects"]
    )
    dp.register_callback_query_handler(
        my_project_page_handler, my_projects_callback.filter()
    )
    dp.register_callback_query_handler(
        delete_project_handler, delete_project_callback.filter()
    )
    dp.register_callback_query_handler(
        vip_project_handler, vip_project_callback.filter()
    )
    dp.register_callback_query_handler(
        price_changing_handler, price_changing_callback.filter()
    )
    dp.register_message_handler(
        delete_confirm_handler, state=DeleteProjectStates.confirm
    )
    dp.register_message_handler(price_changing_state, state=PriceChangingStates.price)
    dp.register_message_handler(
        price_changing_confirm_state, state=PriceChangingStates.confirm
    )
    dp.register_message_handler(vip_need_promo_state, state=VipDiscountStates.is_need)
    dp.register_message_handler(vip_input_promo_state, state=VipDiscountStates.code)
