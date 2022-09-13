import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🗄 Мои предложения")
    btn2 = types.KeyboardButton("💰 Поиск предложений")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text="Здравствуйте, {0.first_name}! Я тестовый бот для продажи покупки проектов!".format(
                         message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def main_menu_handler(message):
    if(message.text == "🗄 Мои предложения"):
        '''
        ВИКИН КОД (вызваешь функцию из файла to_sell)
        '''
        bot.send_message(message.chat.id, text="VIKA...")
    elif(message.text == "💰 Поиск предложений"):
        '''
        ИРИН КОД (вызваешь функцию из файла to_buy)
        '''
        bot.send_message(message.chat.id, text="IRISHKA...")
        
bot.polling(non_stop=True)