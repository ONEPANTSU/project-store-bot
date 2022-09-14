from telebot import types

def sale(message, bot):
    if message.text == "🗄 Мои предложения":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Выставить проект на продажу")
        btn2 = types.KeyboardButton("Список моих предложений")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id,
                     text="Выберите категорию", reply_markup=markup)

    elif message.text == 'Выставить проект на продажу':
        put_up_for_sale(message, bot)
    elif message.text == "Список моих предложений":
        list_for_sale(message, bot)

def put_up_for_sale(message, bot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id,
                     text="Заполните анкету:", reply_markup=markup)
    



def list_for_sale(message, bot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("В разработке...")
    bot.send_message(message.chat.id,
                     text="В разработке...", reply_markup=markup)