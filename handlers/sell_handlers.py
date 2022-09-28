from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from data_base.project import Project
from handlers.main_handlers import get_main_keyboard
from instruments import db_manager
from messages import MESSAGES
from states import SellProjectStates


async def show_main_sell_keyboard(message: Message):
    await message.answer(text=MESSAGES['sell_menu'].format(message.from_user), reply_markup=get_main_sell_keyboard())


def get_main_sell_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    to_sell_project_button = KeyboardButton("Выставить проект на продажу")
    list_of_my_projects_button = KeyboardButton("Список моих предложений")
    back_button = KeyboardButton("Вернуться в главное меню")
    markup.add(to_sell_project_button, list_of_my_projects_button, back_button)
    return markup


async def put_up_for_sale(message: Message):
    await message.answer(text=MESSAGES['put_up_for_sale'].format(message.from_user), reply_markup=get_main_keyboard())
    await message.answer(text=MESSAGES['project_name'])
    await SellProjectStates.project_name.set()


async def project_name_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(project_name=answer)
    await message.answer(text=MESSAGES['price'])
    await SellProjectStates.price.set()


async def price_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(price=answer)
    await message.answer(text=MESSAGES['subscribers'])
    await SellProjectStates.subscribers.set()


async def subscribers_state(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(subscribers=answer)
    await message.answer(text=MESSAGES['themes'])
    await SellProjectStates.themes_names.set()


async def themes_names_state(message: Message, state: FSMContext):
    answer = list()
    answer.append(message.text)
    await state.update_data(themes=answer)
    await message.answer(text=MESSAGES['income'])
    await SellProjectStates.income.set()


async def income_state(message: Message, state: FSMContext):
    answer = message.text
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
    await message.answer(text=MESSAGES['get_list_of_projects'].format(message.from_user),
                         reply_markup=get_main_keyboard())


def register_sell_handlers(dp: Dispatcher):
    dp.register_message_handler(show_main_sell_keyboard, text=['🗄 Мои предложения 🗄'])
    dp.register_message_handler(put_up_for_sale, text=['Выставить проект на продажу'])
    dp.register_message_handler(project_name_state, state=SellProjectStates.project_name)
    dp.register_message_handler(price_state, state=SellProjectStates.price)
    dp.register_message_handler(subscribers_state, state=SellProjectStates.subscribers)
    dp.register_message_handler(themes_names_state, state=SellProjectStates.themes_names)
    dp.register_message_handler(income_state, state=SellProjectStates.income)
    dp.register_message_handler(comment_state, state=SellProjectStates.comment)
    dp.register_message_handler(get_list_of_projects, text=['Список моих предложений'])
