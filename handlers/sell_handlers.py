from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, LabeledPrice, ContentType, PreCheckoutQuery
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from config import PAYMENTS_TOKEN
from data_base.project import Project
from data_base.project import Project, get_projects_list_by_seller_name
from handlers.main_handlers import get_main_keyboard
from instruments import db_manager, bot
from texts.buttons import BUTTONS
from texts.messages import MESSAGES
from states import SellProjectStates

price_amount = 1000
PRICES = [LabeledPrice(label=MESSAGES['sell_payment'], amount=price_amount)]
new_projects_dict = {}


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


async def themes_plus_state(message: Message):
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
    '''
    Подтверждение корректности введённых данных (Да/Нет)
    '''
    await SellProjectStates.buy_process.set()


async def buy_process(message: Message, state: FSMContext):
    data = await state.get_data()
    new_project = Project()
    new_project.name = data['project_name']
    new_project.seller_name = message.from_user.username
    new_project.status_id = 0
    new_project.price = data['price']
    new_project.subscribers = data['subscribers']
    new_project.themes_names = data['themes']
    new_project.income = data['income']
    new_project.comment = data['comment']
    new_projects_dict[message.from_user.username] = new_project
    await bot.send_invoice(message.chat.id,
                           title=MESSAGES['sell_payment_title'],
                           description=MESSAGES['sell_payment_description'],
                           provider_token=PAYMENTS_TOKEN,
                           currency='rub',
                           is_flexible=False,
                           prices=PRICES,
                           start_parameter='example',
                           payload='some_invoice')
    await state.finish()


async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
async def get_list_of_projects(message: Message):
    project_list = get_projects_list_by_seller_name(message.from_user.username)
    await message.reply(text=MESSAGES['get_list_of_projects'], reply_markup=list_of_project_menu())

    #await message.reply()

async def successful_payment(message: Message):
    new_projects_dict[message.from_user.username].save_new_project()
    new_projects_dict.pop(message.from_user.username)
    await bot.send_message(
        message.chat.id,
        MESSAGES['successful_payment'].format(total_amount=message.successful_payment.total_amount // 100,
                                              currency=message.successful_payment.currency)
    )



def list_of_project_menu():
    markup = InlineKeyboardMarkup(row_width = 2)
    prev_button = InlineKeyboardButton(text=BUTTONS['prev'], callback='prev')
    next_button = InlineKeyboardButton(text=BUTTONS['next'], callback='next')
    markup.add(prev_button, next_button)
    return markup


def back_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    back_button = KeyboardButton(BUTTONS['back'])
    markup.add(back_button)
    return markup


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
    dp.register_message_handler(buy_process, state=SellProjectStates.buy_process)
    dp.register_pre_checkout_query_handler(checkout_process, lambda q: True)
    dp.register_message_handler(successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)
