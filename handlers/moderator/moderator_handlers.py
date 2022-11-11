from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from data_base.db_functions import get_moderator_all_project_list, get_moderator_id, set_current_moderator, \
    delete_moderator, set_guarantee
from data_base.project import Project
from handlers.moderator.moderator_callback import moderator_page_callback, chose_moderator_callback, \
    delete_moderator_callback
from handlers.moderator.moderator_functions import get_settings_keyboard, check_is_moderator, get_moderators_keyboard, \
    get_admin_moderators_keyboard, check_is_admin, \
    get_confirmation_menu_keyboard
from handlers.moderator.moderators_carousel import moderators_index, refresh_moderator_pages
from handlers.seller.handlers.sell_handlers import yes_or_no_keyboard
from handlers.seller.inner_functions.seller_carousel_pages import (
    my_project_index,
    refresh_pages,
)
from handlers.seller.instruments.seller_callbacks import verify_callback
from states import ChangeGuaranteeStates
from texts.buttons import BUTTONS
from texts.commands import COMMANDS
from texts.messages import MESSAGES
from useful.commands_handler import commands_handler


async def moderator_handler(message: Message):
    is_moderator = check_is_moderator(message.from_user.id)
    if is_moderator:
        project_list = get_moderator_all_project_list()
        await my_project_index(
            message=message, project_list=project_list, is_moderator=is_moderator
        )


async def verify_callback_handler(query: CallbackQuery, callback_data: dict):
    if check_is_moderator(query.from_user.id):
        project = Project()
        project.set_params_by_id(callback_data.get("id"))
        project.is_verified = 1
        project.save_changes_to_existing_project()
        await refresh_pages(query=query, callback_data=callback_data)


async def settings_handler(message: Message):
    if check_is_moderator(message.from_user.id):
        await message.answer(text=MESSAGES["settings"], reply_markup=get_settings_keyboard())


async def moderator_menu_handler(message: Message):
    if check_is_moderator(message.from_user.id):
        if check_is_admin(message.from_user.id):
            await message.answer(text=MESSAGES["moderators"], reply_markup=get_admin_moderators_keyboard())
        else:
            await message.answer(text=MESSAGES["moderators"], reply_markup=get_moderators_keyboard())
        await moderators_index(message)


async def moderator_page_handler(query: CallbackQuery, callback_data: dict):
    await refresh_moderator_pages(query=query, callback_data=callback_data)


async def chose_moderator_handler(query: CallbackQuery, callback_data: dict):
    if check_is_moderator(query.from_user.id):
        moderator_id = int(callback_data.get("id"))
        set_current_moderator(moderator_id)
        await refresh_moderator_pages(query=query, callback_data=callback_data)


async def delete_moderator_handler(query: CallbackQuery, callback_data: dict):
    if check_is_admin(query.from_user.id):
        moderator_id = int(callback_data.get("id"))
        delete_moderator(moderator_id)
        await refresh_moderator_pages(query=query, callback_data=callback_data)


async def add_moderator_handler(message: Message):
    pass


async def payment_menu_handler(message: Message):
    pass


async def promo_menu_handler(message: Message):
    pass


async def change_guarantee_handler(message: Message):
    await message.answer(text=MESSAGES["change_guarantee"])
    await ChangeGuaranteeStates.ask.set()


async def ask_change_guarantee_state(message: Message, state: FSMContext):
    answer = message.text
    if answer.lstrip("/") in COMMANDS.values():
        await state.finish()
        await commands_handler(message)
    elif answer == BUTTONS["cancel"]:
        await settings_handler(message)
        await state.finish()
    else:
        if answer[0] != "@":
            answer = "@" + answer
            await state.update_data(guarantee=answer)
        else:
            await state.update_data(guarantee=answer)
        await message.answer(MESSAGES["confirm_change_guarantee"],
                             reply_markup=get_confirmation_menu_keyboard())
        await ChangeGuaranteeStates.confirm.set()


async def confirm_change_guarantee_state(message: Message, state: FSMContext):
    answer = message.text
    if answer.lstrip("/") in COMMANDS.values():
        await commands_handler(message)
    elif answer == BUTTONS["confirm"]:
        new_guarantee = await state.get_data()
        set_guarantee(new_guarantee["guarantee"])
        await state.finish()
        await settings_handler(message)
    elif answer == BUTTONS["cancellation"]:
        await state.finish()
        await settings_handler(message)
    else:
        await message.answer(
            text=MESSAGES["command_error"], reply_markup=yes_or_no_keyboard()
        )
        await ChangeGuaranteeStates.confirm.set()


def register_moderator_handlers(dp: Dispatcher):
    dp.register_message_handler(moderator_handler, text=BUTTONS["moderate"])
    dp.register_message_handler(settings_handler, text=BUTTONS["settings"])
    dp.register_message_handler(moderator_menu_handler, text=BUTTONS["moderators"])
    dp.register_message_handler(payment_menu_handler, text=BUTTONS["payment"])
    dp.register_message_handler(promo_menu_handler, text=BUTTONS["promo"])
    dp.register_message_handler(change_guarantee_handler, text=BUTTONS["guarantee"])
    dp.register_callback_query_handler(verify_callback_handler, verify_callback.filter())
    dp.register_callback_query_handler(moderator_page_handler, moderator_page_callback.filter())
    dp.register_message_handler(confirm_change_guarantee_state, state=ChangeGuaranteeStates.confirm)
    dp.register_message_handler(ask_change_guarantee_state, state=ChangeGuaranteeStates.ask)
    dp.register_callback_query_handler(chose_moderator_handler, chose_moderator_callback.filter())
    dp.register_callback_query_handler(delete_moderator_handler, delete_moderator_callback.filter())
    dp.register_message_handler(add_moderator_handler, text=BUTTONS["add_moderator"])
