from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from data_base.project import Project
from handlers.main_handlers import get_main_keyboard
from instruments import db_manager
from texts.buttons import BUTTONS
from texts.messages import MESSAGES
from states import SellProjectStates


async def show_main_sell_keyboard(message: Message):
    await message.answer(text=MESSAGES['sell_menu'].format(message.from_user), reply_markup=get_main_sell_keyboard())


def get_main_sell_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    to_sell_project_button = KeyboardButton(BUTTONS['sell_project'])
    list_of_my_projects_button = KeyboardButton(BUTTONS['sell_list'])
    back_button = KeyboardButton(BUTTONS['back'])
    markup.add(to_sell_project_button, list_of_my_projects_button, back_button)
    return markup


async def put_up_for_sale(message: Message):
    await message.answer(text=MESSAGES['put_up_for_sale'].format(message.from_user), reply_markup=get_main_keyboard())
    await message.answer(text=MESSAGES['project_name'])
    await SellProjectStates.project_name.set()


async def project_name_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(project_name=answer)
    await message.answer(MESSAGES['price'])
    await SellProjectStates.price.set()


async def price_state(message: Message, state: FSMContext):
    answer = message.text
    if not answer.isdigit():
        await message.answer(text=MESSAGES['price_check'])
        await SellProjectStates.price.set()
    else:
        await state.update_data(price=answer)
        await message.answer(text=MESSAGES['subscribers'])
        await SellProjectStates.subscribers.set()


async def subscribers_state(message: Message, state: FSMContext):
    answer = message.text
    if not answer.isdigit():
        await message.answer(text=MESSAGES['subscribers_check'])
        await SellProjectStates.subscribers.set()
    else:
        await state.update_data(subscribers=answer)
        await message.answer(text=MESSAGES['themes'], reply_markup=themes_menu())
        await SellProjectStates.themes_names.set()


async def themes_names_state(message: Message, state: FSMContext):
    themes_dict = db_manager.get_all_themes()
    themes_list = themes_dict.values()
    message_text = message.text
    if set(themes_list) & set(message_text.split()):
        answer = list()
        data = await state.get_data()
        themes = data.get('themes', False)
        if themes:
            answer = data['themes']
        if message.text not in answer:
            answer.append(message.text)
        await state.update_data(themes=answer)
        size = len(answer)
        if size < 3:
            await message.answer(text=MESSAGES['themes_plus'], reply_markup=themes_plus_keyboard())
            await SellProjectStates.themes_plus.set()
        else:
            await message.answer(text=MESSAGES['income'])
            await SellProjectStates.income.set()
    else:

        await message.answer(text=MESSAGES['themes_warn'], reply_markup=themes_menu())
        await SellProjectStates.themes_names.set()


def themes_menu():
    themes_dict = db_manager.get_all_themes()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for key in themes_dict:
        markup.add(KeyboardButton(themes_dict[key]))
    return markup


async def themes_plus_state(message: Message, state: FSMContext):
    answer = message.text
    if answer == "Да":
        await message.answer(text=MESSAGES['themes_plus_1'], reply_markup=themes_menu())
        await SellProjectStates.themes_names.set()
    elif answer == "Нет":
        await message.answer(text=MESSAGES['income'])
        await SellProjectStates.income.set()


def themes_plus_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    yes_button = KeyboardButton(BUTTONS['yes'])
    no_button = KeyboardButton(BUTTONS['no'])
    markup.add(yes_button, no_button)
    return markup


async def income_state(message: Message, state: FSMContext):
    answer = message.text
    if not answer.isdigit():
        await message.answer(text=MESSAGES['income_check'])
        await SellProjectStates.income.set()
    else:
        await state.update_data(income=answer)
        await message.answer(text=MESSAGES['comment'])
        await SellProjectStates.comment.set()


async def comment_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(comment=answer)
    await message.answer(text=MESSAGES['save_project'])
    project = Project(db_manager)
    data = await state.get_data()
    project.name = data['project_name']
    project.seller_name = message.from_user.username
    project.status_id = 0
    project.price = data['price']
    project.subscribers = data['subscribers']
    project.themes_names = data['themes']
    project.income = data['income']
    project.comment = data['comment']
    project.save_new_project()

    await state.finish()


async def get_list_of_projects(message: Message):
    proj = db_manager.get_projects_by_seller_id(message.from_user.id)
    await message.reply('Data: {}'.format(proj))
    #await message.answer(text=MESSAGES['get_list_of_projects'].format(message.from_user),
                         #reply_markup=get_main_keyboard())


def register_sell_handlers(dp: Dispatcher):
    dp.register_message_handler(show_main_sell_keyboard, text=[BUTTONS['sell_menu']])
    dp.register_message_handler(put_up_for_sale, text=[BUTTONS['sell_project']])
    dp.register_message_handler(project_name_state, state=SellProjectStates.project_name)
    dp.register_message_handler(price_state, state=SellProjectStates.price)
    dp.register_message_handler(subscribers_state, state=SellProjectStates.subscribers)
    dp.register_message_handler(themes_names_state, state=SellProjectStates.themes_names)
    dp.register_message_handler(themes_plus_state, state=SellProjectStates.themes_plus)
    dp.register_message_handler(income_state, state=SellProjectStates.income)
    dp.register_message_handler(comment_state, state=SellProjectStates.comment)
    dp.register_message_handler(get_list_of_projects, text=[BUTTONS['sell_list']])
