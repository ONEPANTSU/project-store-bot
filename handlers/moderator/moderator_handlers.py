from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from data_base.db_functions import (
    add_moderator,
    add_promo_code,
    delete_moderator,
    get_moderator_all_project_list,
    set_current_moderator,
    set_guarantee,
)
from data_base.project import Project
from handlers.moderator.moderator_callback import (
    add_promo_callback,
    chose_moderator_callback,
    delete_moderator_callback,
    delete_promo_callback,
    moderator_page_callback,
)
from handlers.moderator.moderator_functions import (
    check_is_admin,
    check_is_moderator,
    get_admin_moderators_keyboard,
    get_cancel_keyboard,
    get_confirmation_menu_keyboard,
    get_moderators_keyboard,
    get_payment_menu_keyboard,
    get_promo_keyboard,
    get_promo_type_keyboard,
    get_settings_keyboard,
)
from handlers.moderator.moderators_carousel import (
    moderators_index,
    refresh_moderator_pages,
)
from handlers.seller.inner_functions.seller_carousel_pages import (
    my_project_index,
    refresh_pages,
)
from handlers.seller.instruments.seller_callbacks import verify_callback
from states import AddModeratorStates, ChangeGuaranteeStates, ChangePaymentStates, DeletePromoStates
from states.add_promo_states import AddPromoStates
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
        await message.answer(
            text=MESSAGES["settings"], reply_markup=get_settings_keyboard()
        )


async def moderator_menu_handler(message: Message):
    if check_is_moderator(message.from_user.id):
        if check_is_admin(message.from_user.id):
            await message.answer(
                text=MESSAGES["moderators"],
                reply_markup=get_admin_moderators_keyboard(),
            )
        else:
            await message.answer(
                text=MESSAGES["moderators"], reply_markup=get_moderators_keyboard()
            )
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
    if check_is_moderator(message.from_user.id):
        await message.answer(
            text=MESSAGES["id_add_moderator"], reply_markup=get_cancel_keyboard()
        )
        await AddModeratorStates.id.set()


async def id_add_moderator_handler(message: Message, state: FSMContext):
    if check_is_moderator(message.from_user.id):
        answer = message.text
        if answer.lstrip("/") in COMMANDS.values():
            await state.finish()
            await commands_handler(message)
        elif answer == BUTTONS["cancel"]:
            await settings_handler(message)
            await state.finish()
        else:
            if not answer.isdigit():
                await message.answer(text=MESSAGES["id_check"])
                await AddModeratorStates.id.set()
            else:
                await state.update_data(id=answer)
                await message.answer(
                    MESSAGES["name_add_moderator"],
                    reply_markup=get_confirmation_menu_keyboard(),
                )
                await AddModeratorStates.name.set()


async def name_add_moderator_handler(message: Message, state: FSMContext):
    if check_is_moderator(message.from_user.id):
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
            await state.update_data(name=answer)
            await message.answer(
                MESSAGES["confirm_add_moderator"],
                reply_markup=get_confirmation_menu_keyboard(),
            )
            await AddModeratorStates.confirm.set()


async def confirm_add_moderator_state(message: Message, state: FSMContext):
    if check_is_moderator(message.from_user.id):
        answer = message.text
        if answer.lstrip("/") in COMMANDS.values():
            await state.finish()
            await commands_handler(message)
        elif answer == BUTTONS["confirm"]:
            new_moderator = await state.get_data()
            add_moderator(new_moderator["id"], new_moderator["name"])
            await state.finish()
            await message.answer(text=MESSAGES["update_save"])
            await settings_handler(message)
        elif answer == BUTTONS["cancellation"]:
            await state.finish()
            await settings_handler(message)
        else:
            await message.answer(
                text=MESSAGES["command_error"],
                reply_markup=get_confirmation_menu_keyboard(),
            )
            await AddModeratorStates.confirm.set()


async def payment_menu_handler(message: Message):
    if check_is_moderator(message.from_user.id):
        await message.answer(
            text=MESSAGES["change_payment"], reply_markup=get_payment_menu_keyboard()
        )
        await ChangePaymentStates.ask.set()


async def ask_change_payment_state_handler(message: Message, state: FSMContext):
    if check_is_moderator(message.from_user.id):
        answer = message.text
        if answer.lstrip("/") in COMMANDS.values():
            await state.finish()
            await commands_handler(message)
        elif answer == BUTTONS["cancel"]:
            await settings_handler(message)
            await state.finish()
        elif answer == BUTTONS["change_regular_price"]:
            await message.answer(text=MESSAGES["new_payment"])
            await ChangePaymentStates.regular.set()
        elif answer == BUTTONS["change_vip_price"]:
            await message.answer(text=MESSAGES["new_payment"])
            await ChangePaymentStates.vip.set()
        else:
            await message.answer(MESSAGES["not_recognized"])
            await message.answer(
                text=MESSAGES["change_payment"],
                reply_markup=get_payment_menu_keyboard(),
            )
            await ChangePaymentStates.ask.set()


async def regular_change_payment_state_handler(message: Message, state: FSMContext):
    if check_is_moderator(message.from_user.id):
        answer = message.text
        if answer.lstrip("/") in COMMANDS.values():
            await state.finish()
            await commands_handler(message)
        else:
            if not answer.isdigit():
                await message.answer(text=MESSAGES["payment_check"])
                await ChangePaymentStates.regular.set()
            else:
                answer = int(answer) * 100
                await state.update_data(regular=answer)
                await state.update_data(type="regular")
            await message.answer(
                MESSAGES["confirm_change_payment"],
                reply_markup=get_confirmation_menu_keyboard(),
            )
            await ChangePaymentStates.confirm.set()


async def vip_change_payment_state_handler(message: Message, state: FSMContext):
    if check_is_moderator(message.from_user.id):
        answer = message.text
        if answer.lstrip("/") in COMMANDS.values():
            await state.finish()
            await commands_handler(message)
        else:
            if not answer.isdigit():
                await message.answer(text=MESSAGES["payment_check"])
                await ChangePaymentStates.vip.set()
            else:
                answer = int(answer) * 100
                await state.update_data(regular=answer)
                await state.update_data(type="vip")
            await message.answer(
                MESSAGES["confirm_change_payment"],
                reply_markup=get_confirmation_menu_keyboard(),
            )
            await ChangePaymentStates.confirm.set()


async def confirm_change_payment_state(message: Message, state: FSMContext):
    if check_is_moderator(message.from_user.id):
        answer = message.text
        if answer.lstrip("/") in COMMANDS.values():
            await commands_handler(message)
        elif answer == BUTTONS["confirm"]:
            data = await state.get_data()
            if data["type"] == "regular":
                pass
                # сохранение для простой цены
            else:
                pass
                # сохранение для простой цены
            await state.finish()
            await message.answer(text=MESSAGES["update_save"])
            await settings_handler(message)
        elif answer == BUTTONS["cancellation"]:
            await state.finish()
            await settings_handler(message)
        else:
            await message.answer(
                text=MESSAGES["command_error"],
                reply_markup=get_confirmation_menu_keyboard(),
            )
            await ChangePaymentStates.confirm.set()


async def promo_menu_handler(message: Message):
    if check_is_moderator(message.from_user.id):
        text = "Промокоды:"
        await message.answer(text=text, reply_markup=get_promo_keyboard())


async def add_promo_handler(query: CallbackQuery):
    if check_is_moderator(query.from_user.id):
        await query.message.answer(
            text="Выберите тип промокода:", reply_markup=get_promo_type_keyboard()
        )
        await AddPromoStates.type.set()


async def type_add_promo_handler(message: Message, state: FSMContext):
    if check_is_moderator(message.from_user.id):
        answer = message.text
        if answer.lstrip("/") in COMMANDS.values():
            await state.finish()
            await commands_handler(message)
        elif answer == "%" or answer == "₽":
            if answer == "%":
                await state.update_data(type=0)
                await message.answer(
                    text="Введите процент скидки (%):",
                    reply_markup=get_cancel_keyboard(),
                )
            else:
                await state.update_data(type=1)
                await message.answer(
                    text="Введите скидку в рублях (₽):",
                    reply_markup=get_cancel_keyboard(),
                )
            await AddPromoStates.discount.set()
        elif answer == BUTTONS["cancellation"]:
            await state.finish()
            await settings_handler(message)
        else:
            await message.answer(
                text=MESSAGES["command_error"], reply_markup=get_promo_type_keyboard()
            )
            await AddPromoStates.type.set()


async def discount_add_promo_handler(message: Message, state: FSMContext):
    if check_is_moderator(message.from_user.id):
        answer = message.text
        if answer.lstrip("/") in COMMANDS.values():
            await state.finish()
            await commands_handler(message)
        elif answer == BUTTONS["cancel"]:
            await settings_handler(message)
            await state.finish()
        else:
            if not answer.isdigit():
                await message.answer(text="Скидка должна быть числом!")
                await AddPromoStates.discount.set()
            else:
                await state.update_data(discount=answer)
                await message.answer(
                    "Введите текст промокода:", reply_markup=get_cancel_keyboard()
                )
                await AddPromoStates.code.set()


async def code_add_promo_handler(message: Message, state: FSMContext):
    if check_is_moderator(message.from_user.id):
        answer = message.text
        if answer.lstrip("/") in COMMANDS.values():
            await state.finish()
            await commands_handler(message)
        elif answer == BUTTONS["cancel"]:
            await state.finish()
            await settings_handler(message)
        else:
            await state.update_data(code=answer)
            data = await state.get_data()
            text = (
                "Данные введены верно?\n\n"
                + data.get("code")
                + " ~ <b>"
                + data.get("discount")
            )
            if data.get("type") == 0:
                text += "% </b>"
            elif data.get("type") == 1:
                text += "₽ </b>"

            await message.answer(
                text=text, reply_markup=get_confirmation_menu_keyboard()
            )
            await AddPromoStates.confirm.set()


async def confirm_add_promo_handler(message: Message, state: FSMContext):
    if check_is_moderator(message.from_user.id):
        answer = message.text
        if answer.lstrip("/") in COMMANDS.values():
            await state.finish()
            await commands_handler(message)
        elif answer == BUTTONS["confirm"]:
            new_promo = await state.get_data()
            add_promo_code(
                new_promo["code"], int(new_promo["discount"]), new_promo["type"]
            )
            await state.finish()
            await message.answer(text=MESSAGES["update_save"])
            await settings_handler(message)
        elif answer == BUTTONS["cancellation"]:
            await state.finish()
            await settings_handler(message)
        else:
            await message.answer(
                text=MESSAGES["command_error"],
                reply_markup=get_confirmation_menu_keyboard(),
            )
            await AddPromoStates.confirm.set()


async def delete_promo_handler(query: CallbackQuery, callback_data: dict, state: FSMContext):
    code = callback_data.get("code")
    await query.message.answer(
        text=MESSAGES["delete_promo"].format(code=code), reply_markup=get_confirmation_menu_keyboard()
    )
    await state.update_data(code=code)
    await DeletePromoStates.confirm.set()


async def confirm_delete_promo_state(message: Message, state: FSMContext):
    if check_is_moderator(message.from_user.id):
        answer = message.text
        if answer.lstrip("/") in COMMANDS.values():
            await state.finish()
            await commands_handler(message)
        elif answer == BUTTONS["confirm"]:
            data = await state.get_data()
            #сохранение
            await state.finish()
            await message.answer(text=MESSAGES["update_save"])
            await settings_handler(message)
        elif answer == BUTTONS["cancellation"]:
            await state.finish()
            await settings_handler(message)
        else:
            await message.answer(
                text=MESSAGES["command_error"],
                reply_markup=get_confirmation_menu_keyboard(),
            )
            await DeletePromoStates.confirm.set()


async def change_guarantee_handler(message: Message):
    if check_is_moderator(message.from_user.id):
        await message.answer(
            text=MESSAGES["change_guarantee"], reply_markup=get_cancel_keyboard()
        )
        await ChangeGuaranteeStates.ask.set()


async def ask_change_guarantee_state(message: Message, state: FSMContext):
    if check_is_moderator(message.from_user.id):
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
            await message.answer(
                MESSAGES["confirm_change_guarantee"],
                reply_markup=get_confirmation_menu_keyboard(),
            )
            await ChangeGuaranteeStates.confirm.set()


async def confirm_change_guarantee_state(message: Message, state: FSMContext):
    if check_is_moderator(message.from_user.id):
        answer = message.text
        if answer.lstrip("/") in COMMANDS.values():
            await commands_handler(message)
        elif answer == BUTTONS["confirm"]:
            new_guarantee = await state.get_data()
            set_guarantee(new_guarantee["guarantee"])
            await state.finish()
            await message.answer(text=MESSAGES["update_save"])
            await settings_handler(message)
        elif answer == BUTTONS["cancellation"]:
            await state.finish()
            await settings_handler(message)
        else:
            await message.answer(
                text=MESSAGES["command_error"],
                reply_markup=get_confirmation_menu_keyboard(),
            )
            await ChangeGuaranteeStates.confirm.set()


def register_moderator_handlers(dp: Dispatcher):
    dp.register_message_handler(moderator_handler, text=BUTTONS["moderate"])
    dp.register_message_handler(settings_handler, text=BUTTONS["settings"])
    dp.register_message_handler(moderator_menu_handler, text=BUTTONS["moderators"])
    dp.register_message_handler(payment_menu_handler, text=BUTTONS["payment"])
    dp.register_message_handler(promo_menu_handler, text=BUTTONS["promo"])
    dp.register_message_handler(change_guarantee_handler, text=BUTTONS["guarantee"])
    dp.register_callback_query_handler(
        verify_callback_handler, verify_callback.filter()
    )
    dp.register_callback_query_handler(
        moderator_page_handler, moderator_page_callback.filter()
    )
    dp.register_message_handler(id_add_moderator_handler, state=AddModeratorStates.id)
    dp.register_message_handler(
        name_add_moderator_handler, state=AddModeratorStates.name
    )
    dp.register_message_handler(
        confirm_add_moderator_state, state=AddModeratorStates.confirm
    )
    dp.register_message_handler(
        ask_change_payment_state_handler, state=ChangePaymentStates.ask
    )
    dp.register_message_handler(
        regular_change_payment_state_handler, state=ChangePaymentStates.regular
    )
    dp.register_message_handler(
        vip_change_payment_state_handler, state=ChangePaymentStates.vip
    )
    dp.register_message_handler(
        confirm_change_payment_state, state=ChangePaymentStates.confirm
    )
    dp.register_message_handler(
        ask_change_guarantee_state, state=ChangeGuaranteeStates.ask
    )
    dp.register_message_handler(
        confirm_change_guarantee_state, state=ChangeGuaranteeStates.confirm
    )
    dp.register_callback_query_handler(
        chose_moderator_handler, chose_moderator_callback.filter()
    )
    dp.register_callback_query_handler(
        delete_moderator_handler, delete_moderator_callback.filter()
    )
    dp.register_message_handler(add_moderator_handler, text=BUTTONS["add_moderator"])
    dp.register_callback_query_handler(add_promo_handler, add_promo_callback.filter())
    dp.register_message_handler(type_add_promo_handler, state=AddPromoStates.type)
    dp.register_message_handler(
        discount_add_promo_handler, state=AddPromoStates.discount
    )
    dp.register_message_handler(code_add_promo_handler, state=AddPromoStates.code)
    dp.register_message_handler(confirm_add_promo_handler, state=AddPromoStates.confirm)
    dp.register_message_handler(confirm_delete_promo_state, state=DeletePromoStates.confirm)
    dp.register_callback_query_handler(
        delete_promo_handler, delete_promo_callback.filter()
    )
