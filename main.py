import telebot # Импортируем telebot
from telebot import types
import random # для выбора случайного комплимента
from compliments import compliments
from secret import secrets


token = secrets.get('BOT_API_TOKEN')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("Старт")
    action_button = types.KeyboardButton("Комплимент")
    markup.add(start_button, action_button)
    bot.send_message(message.chat.id, text="Привет, {0.first_name} \nВоспользуйся кнопками".format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def buttons(message):
    if (message.text == "Старт"):
        bot.send_message(message.chat.id, text="Я могу поддержать тебя и поднять настроение. Просто попроси об этом")
    elif (message.text == "Комплимент"):
        bot.send_message(message.chat.id, text=f"{random.choice(compliments)}")
    else:
        bot.send_message(message.chat.id, text="Пока что, я могу отвечать только на команды с кнопок")


@bot.message_handler(content_types=['img'])
def buttons(message):
    bot.send_message(message.chat.id, text="Выглядит интересно... Что это?")

bot.polling(none_stop=True, interval=0)