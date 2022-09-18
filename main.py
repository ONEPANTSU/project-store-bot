from telebot import types
import telebot
import config
from data_base.project import Project

bot = telebot.TeleBot(config.TOKEN)


def show_main_keyboard(message, text):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    my_projects_button = types.KeyboardButton("🗄 Мои предложения 🗄")
    search_projects_button = types.KeyboardButton("💰 Поиск предложений 💰")
    markup.add(my_projects_button, search_projects_button)
    bot.send_message(message.chat.id,
                     text=text, reply_markup=markup)


@bot.message_handler(commands=['start'])
def main_menu(message):
    text = "Здравствуйте, {0.first_name}! Я тестовый бот для продажи и покупки проектов!" \
        .format(message.from_user)
    show_main_keyboard(message, text)
    bot.send_message(message.chat.id, text="📌 Главное меню 📌")


@bot.message_handler(content_types=['text'])
def main_menu_handler(message):
    if message.text == "🗄 Мои предложения 🗄":
        show_main_sell_keyboard(message)
        bot.register_next_step_handler(message, main_sell_handler)

    elif message.text == "💰 Поиск предложений 💰":
        show_main_buy_keyboard(message)
        bot.register_next_step_handler(message, main_buy_handler)


"""
ВИКИНА ЧАСТЬ:
"""


def show_main_sell_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    to_sell_project_button = types.KeyboardButton("Выставить проект на продажу")
    list_of_my_projects_button = types.KeyboardButton("Список моих предложений")
    back_button = types.KeyboardButton("Вернуться в главное меню")
    markup.add(to_sell_project_button, list_of_my_projects_button, back_button)
    bot.send_message(message.chat.id, '🗄 Ваши проекты 🗄', reply_markup=markup)


def main_sell_handler(message):
    if message.text == "Выставить проект на продажу":
        bot.register_next_step_handler(message, put_up_for_sale)
    elif message.text == "Список моих предложений":
        bot.register_next_step_handler(message, get_list_of_projects)
    elif message.text == "Вернуться в главное меню":
        show_main_keyboard(message, "📌 Главное меню 📌")
        bot.register_next_step_handler(message, main_menu_handler)


def put_up_for_sale(message):
    pass


def get_list_of_projects(message):
    pass


"""
ИРИНА ЧАСТЬ:
"""


def show_main_buy_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("...1")
    button2 = types.KeyboardButton("...2")
    back_button = types.KeyboardButton("Вернуться в главное меню")
    markup.add(button1, button2, back_button)
    bot.send_message(message.chat.id, '💰 Поиск предложений 💰', reply_markup=markup)


def main_buy_handler(message):
    if message.text == "...1":
        pass
        # bot.register_next_step_handler(message, )
    elif message.text == "...2":
        pass
        # bot.register_next_step_handler(message, )
    elif message.text == "Вернуться в главное меню":
        show_main_keyboard(message, "📌 Главное меню 📌")
        bot.register_next_step_handler(message, main_menu_handler)


bot.polling(non_stop=True)
