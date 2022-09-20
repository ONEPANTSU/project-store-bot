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
ВИКИНА ЧАСТЬ: всё будет супер!!!!!!
"""
project = Project()

def show_main_sell_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    to_sell_project_button = types.KeyboardButton("Выставить проект на продажу")
    list_of_my_projects_button = types.KeyboardButton("Список моих предложений")
    back_button = types.KeyboardButton("Вернуться в главное меню")
    markup.add(to_sell_project_button, list_of_my_projects_button, back_button)
    bot.send_message(message.chat.id, '🗄 Ваши проекты 🗄', reply_markup=markup)


def main_sell_handler(message):
    if message.text == "Выставить проект на продажу":
        put_up_for_sale(message)
    elif message.text == "Список моих предложений":
        bot.register_next_step_handler(message, get_list_of_projects)
    elif message.text == "Вернуться в главное меню":
        show_main_keyboard(message, "📌 Главное меню 📌")
        bot.register_next_step_handler(message, main_menu_handler)


def put_up_for_sale(message):
    bot.send_message(message.chat.id, text="🖊Заполните анкету🖊:")
    project.seller_name = "@" + message.from_user.username
    project.status_id = 0
    message = bot.send_message(message.chat.id,
                               text="Напишите название вашего проекта:")
    bot.register_next_step_handler(message, process_name_step)

def process_name_step(message):
    project.name = message.text
    message = bot.send_message(message.chat.id,
                            text="Напишите цену вашего проекта?")
    bot.register_next_step_handler(message, process_price_step)


def process_price_step(message):
    price = message.text
    project.price = message.text
    if not price.isdigit():
        message = bot.reply_to(message, 'Цена должна быть числом. Напишите цену вашего проекта:')
        bot.register_next_step_handler(message, process_price_step)
        return
    message = bot.send_message(message.chat.id,
                               text="Сколько подписчиков у вашего проекта?")
    bot.register_next_step_handler(message, process_subscribers_step)

def process_subscribers_step(message):
    subscribers = message.text
    project.subscribers = message.text
    if not subscribers.isdigit():
        message = bot.reply_to(message, 'Укажите количество подписчиков числом. Напишите сколько подписчиков у вашего проекта:')
        bot.register_next_step_handler(message, process_subscribers_step)
        return
    message = bot.send_message(message.chat.id,
                               text="Укажите тему или темы вашего проекта:")
    bot.register_next_step_handler(message, process_themes_id_step)

def process_themes_id_step(message):
    #choose_themes(message)
    project.themes_id = message.text
    message = bot.send_message(message.chat.id,
                               text="Какой доход у вашего проекта?")
    bot.register_next_step_handler(message, process_income_step)

# def choose_themes_menu(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     theme_button_1 = types.KeyboardButton("Криптовалюта")
#     theme_button_2 = types.KeyboardButton("Выставить проект на продажу")
#     theme_button_3 = types.KeyboardButton("Выставить проект на продажу")
#     theme_button_4 = types.KeyboardButton("Выставить проект на продажу")
#     markup.add()
#     bot.send_message(message.chat.id, '🗄 Ваши проекты 🗄', reply_markup=markup)

#def choose_themes(message):


def process_income_step(message):
    income = message.text
    project.income = message.text
    if not income.isdigit():
        message = bot.reply_to(message, 'Укажите доход проекта числом. Какой доход у вашего проекта:')
        bot.register_next_step_handler(message, process_income_step)
        return
    message = bot.send_message(message.chat.id,
                               text="Добавьте комментарий к обьявлению:")
    bot.register_next_step_handler(message, process_comment_step)

def process_comment_step(message):
    project.comment = message.text
    message = bot.send_message(message.chat.id,
                               text="Ваше обьявление сохранено!")
    bot.register_next_step_handler(message, process_save_step)

def process_save_step(message):
    message = bot.send_message(message.chat.id,
                               text="Вы вернулись в главное меню")
    main_menu_handler(message)
    project.save_new_project()

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
