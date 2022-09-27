from telebot import types
import telebot
import config
from data_base.db_manager import DBManager
from data_base.project import Project, get_projects_list_by_seller_name, get_projects_list_by_themes_id

bot = telebot.TeleBot(config.TOKEN)
db_manager = DBManager()


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
    bot.send_message(message.chat.id, text="🖊Заполните анкету🖊")
    project = Project(db_manager)
    project.themes_names = list()
    project.seller_name = "@" + message.from_user.username
    project.status_id = 0
    message = bot.send_message(message.chat.id,
                               text="Напишите название вашего проекта")
    bot.register_next_step_handler(message, process_name_step, project)


def process_name_step(message, project):
    project.name = message.text
    message = bot.send_message(message.chat.id,
                               text="Напишите цену вашего проекта")
    bot.register_next_step_handler(message, process_price_step, project)


def process_price_step(message, project):
    price = message.text
    project.price = message.text
    if not price.isdigit():
        message = bot.reply_to(message, 'Цена должна быть числом. Напишите цену вашего проекта:')
        bot.register_next_step_handler(message, process_price_step, project)
        return
    message = bot.send_message(message.chat.id,
                               text="Сколько подписчиков у вашего проекта?")
    bot.register_next_step_handler(message, process_subscribers_step, project)


def process_subscribers_step(message, project):
    subscribers = message.text
    project.subscribers = message.text
    if not subscribers.isdigit():
        message = bot.reply_to(message,
                               'Укажите количество подписчиков числом. Напишите сколько подписчиков у вашего проекта:')
        bot.register_next_step_handler(message, process_subscribers_step, project)
        return
    message = bot.send_message(message.chat.id,
                               text="Укажите тему или темы вашего проекта:")
    choose_themes(message, project)


def choose_themes(message, project):
    text = 'Список тем'
    choose_themes_menu1(message, text)
    bot.register_next_step_handler(message, choose_themes_menu2, project)


def choose_themes_menu1(message, text):
    markup = types.ReplyKeyboardMarkup()
    theme_button_1 = types.KeyboardButton("Криптовалюта")
    theme_button_2 = types.KeyboardButton("Недвижимость")
    theme_button_3 = types.KeyboardButton("Маркетинг")
    theme_button_4 = types.KeyboardButton("Бизнес/Финансы")
    markup.add(theme_button_1, theme_button_2, theme_button_3, theme_button_4)
    bot.send_message(message.chat.id, text=text, reply_markup=markup)


def choose_themes_menu2(message, project):
    themes_name = message.text
    project.themes_names.append(themes_name)
    project.themes_id = DBManager().get_themes_id_by_names(project.themes_names)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes_button = types.KeyboardButton("Да")
    no_button = types.KeyboardButton("Нет")
    markup.add(yes_button, no_button)
    bot.send_message(message.chat.id, 'Хотите выбрать ещё тему?', reply_markup=markup)
    bot.register_next_step_handler(message, choose_themes_menu3, project)


def choose_themes_menu3(message, project):
    if message.text == "Да":
        choose_themes(message, project)
        # bot.register_next_step_handler(message, process_income_step, project)

    elif message.text == "Нет":
        message = bot.send_message(message.chat.id,
                                   text="Какой доход у вашего проекта?")
        bot.register_next_step_handler(message, process_income_step, project)


def process_income_step(message, project):
    income = message.text
    project.income = message.text
    if not income.isdigit():
        message = bot.reply_to(message, 'Укажите доход проекта числом. Какой доход у вашего проекта:')
        bot.register_next_step_handler(message, process_income_step, project)
        return
    message = bot.send_message(message.chat.id,
                               text="Добавьте комментарий к обьявлению:")
    bot.register_next_step_handler(message, process_comment_step, project)


def process_comment_step(message, project):
    project.comment = message.text
    message = bot.send_message(message.chat.id,
                               text="Ваше обьявление сохранено!")
    bot.register_next_step_handler(message, process_save_step, project)


def process_save_step(message, project):
    message = bot.send_message(message.chat.id,
                               text="Вы вернулись в главное меню")
    main_menu_handler(message)
    print(project.name)
    project.save_new_project()


def get_list_of_projects(message):
    pass


"""
ИРИНА ЧАСТЬ: охаёёёёёёёёёёё они чан
"""


def show_main_buy_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    category_button = types.KeyboardButton("Выбрать тематику")
    price_range_button = types.KeyboardButton("Выбрать ценовой диапазон")
    back_button = types.KeyboardButton("Вернуться в главное меню")
    markup.add(category_button, price_range_button, back_button)
    bot.send_message(message.chat.id, '💰 Поиск предложений 💰', reply_markup=markup)


def main_buy_handler(message):
    if message.text == "Выбрать тематику":
        choose_category(message)
    elif message.text == "Выбрать ценовой диапазон":
        choose_price_range(message)
    elif message.text == "Вернуться в главное меню":
        show_main_keyboard(message, "📌 Главное меню 📌")
        bot.register_next_step_handler(message, main_menu_handler)


# Действия после нажатия кнопки "Выбрать тематику"
def choose_category(message):
    # С помощью функции get_all_themes() присваиваем в themes - словарь с темами и их айди
    themes = DBManager().get_all_themes()
    button_list = []
    # Заполнение списка тем из словаря с базы данных
    for i in themes.keys():
        button_list.append(types.InlineKeyboardButton(text=themes[i], callback_data="ch_ct{}".format(i)))

    # # сборка клавиатуры из кнопок `InlineKeyboardButton`
    reply_markup = types.InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    # отправка клавиатуры в чат
    bot.send_message(message.chat.id, text="Выберите интересные тематики", reply_markup=reply_markup)


# Функция построения меню в сообщении
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


@bot.callback_query_handler(func=lambda call: True)
def theme_handler(call):
    theme_id = int(call.data[5:])
    bot.send_message(call.message.chat.id, 'Data: {}'.format(str(call.data)))
    bot.answer_callback_query(call.id)


# Действия после нажатия кнопки "Выбрать ценовой диапазон"
def choose_price_range(message):
    pass


bot.polling(non_stop=True)
