import telebot # Импортируем telebot
from telebot import types
import random # для выбора случайного комплимента
import requests
import datetime


from compliments import compliments
from secret import secrets
from inline_btns import CATALOG_FOR_UNKNOWN_MESSAGE
from commands import *

token = secrets.get('BOT_API_TOKEN')
bot = telebot.TeleBot(token)
token_weather = secrets.get('OPEN_WEATHER_MAP_TOKEN')



@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("Что умеешь?")
    action_button = types.KeyboardButton("Хочу комплимент")
    markup.add(start_button, action_button)
    bot.send_message(message.chat.id, text="Привет, {0.first_name} \nВоспользуйся кнопками".format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def buttons(message):


    def get_weather(city = "moscow", token = token_weather):
        try:
            r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}&units=metric")
            data = r.json()
            city = data["name"]
            country = data["sys"]["country"]
            temp = data["main"]["temp"]
            temp_feel = data["main"]["feels_like"]
            pressure = data["main"]["pressure"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            lendth_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

            weather = f"***{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}***\nПогода в городе {city}({country})\nТемперетура: {temp}°С, ощущается как {temp_feel}°С\nДавление: {pressure}мм.рт.ст\nВлажность: {humidity}%\nСкорость ветра {wind_speed}м/с\nВосход солнца: {sunrise}\nЗакат Солнца: {sunset}\nПродолжительность дня: {lendth_of_the_day}\n \U0001F607 Удачи! \U0001F607"
            bot.send_message(message.chat.id, text=f"{weather}")
        except Exception as ex:
            bot.send_message(message.chat.id, text=f"\U00002620 error!! {ex} \U00002620")


    match message.text:
        case "Что умеешь?":
            bot.send_message(message.chat.id, text="Я могу поддержать тебя и поднять настроение. Просто попроси об этом.")

        case "Хочу комплимент":
            bot.send_message(message.chat.id, text=f"{random.choice(compliments)}")

        case "Забей":
            bot.reply_to(message, no_comment())

        case "Не важно":
            bot.reply_to(message, no_comment())

        case "Гав":
            bot.reply_to(message, "Мяу.")

        case "Мяу":
            bot.reply_to(message, "Ну допустим, мяу.")
        
        case _:
            callback_message = message.text
            bot.send_message(message.chat.id, text=f"Пока что, я не знаю что ответить на '{callback_message}'. Придумай что-нибудь получше.")
            markup = types.InlineKeyboardMarkup(row_width=1)
            

            btn3 = types.InlineKeyboardButton("Забей", callback_data="nothing")

            markup.add(btn3)
            bot.reply_to(message, "Что мне делать с этой информацией?", reply_markup=markup)

    #if "tiktok.com" in message.text or "youtube.com" in message.text or "youtu.be" in message.text :
    #   video = download(message.text)
     #   bot.reply_to(message, video)

            if "что" in message.text or "Что" in message.text:
                bot.reply_to(message, "Что?")
            
            if "Погода " in message.text or "погода " in message.text:
                bot.reply_to(message, "А хотя...")
                city = message.text.split()
                city = translate(city[-1], -1, "en")
                get_weather(city)




@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        match call.data:
            case "nothing":
                bot.send_message(call.message.chat.id, no_comment())
                




bot.polling(none_stop=True, interval=0)