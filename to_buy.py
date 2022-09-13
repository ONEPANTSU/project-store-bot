from telebot import types




def buy_menu(message, bot):
    if message.text == "💰 Поиск предложений":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        bt1 = types.KeyboardButton("Выбрать категорию")
        bt2 = types.KeyboardButton("Выбрать ценовой диапазон")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(bt1, bt2, back)
        bot.send_message(message.chat.id, text="Выберите действие", reply_markup=markup)

    elif message.text == "Выбрать категорию":

        ##########
        # список кнопок
        button_list = [
            types.InlineKeyboardButton(text="Category 1", callback_data='fjnd'),
            types.InlineKeyboardButton(text="Category 2", callback_data='dujfd'),
            types.InlineKeyboardButton(text="Category 3",callback_data='fcjdsu')
        ]

        # сборка клавиатуры из кнопок `InlineKeyboardButton`
        reply_markup = types.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
        # отправка клавиатуры в чат
        bot.send_message(message.chat.id, text="Меню Категорий", reply_markup=reply_markup)

        ##########
    elif message.text == "Выбрать ценовой диапазон":

        ##########
        bot.send_message(message.chat.id, "...........В разработке..................")
        ##########

    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("🗄 Мои предложения")
        button2 = types.KeyboardButton("💰 Поиск предложений")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)

def build_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu
