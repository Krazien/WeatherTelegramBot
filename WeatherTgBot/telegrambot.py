import telebot
from telebot import types
import os
from dotenv import load_dotenv

from DataBase.DataBase_manager import DataBase

load_dotenv()

TOKEN = os.getenv('TOKEN')

if not TOKEN:
    raise ValueError('API токен не найден! Проверь файл .env')
# token = '7720424435:AAFBMZ0nei9lIxCMMsqMi5qL_3d4jOsclNk'

# Экземпляр бота
bot = telebot.TeleBot(TOKEN)

DataBase_manager = DataBase()
DataBase_manager.create_table_users()
DataBase_manager.create_table_messages()
DataBase_manager.create_table_city()


@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    DataBase_manager.save_user(user)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Поздороваться')
    markup.add(btn1)
    bot.reply_to(message, f'Привет, я твой погодный бот.🌍 Обращайся😉', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def response(message):
    user = message.from_user
    DataBase_manager.save_message(user.id, message.message_id, message.text, message.date)
    if message.text == 'Выбрать действие':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Задать город проживания')
        btn2 = types.KeyboardButton('Найти погоду в интересуещем городе')
        markup.add(btn1, btn2)
        bot.reply_to(message, 'Что вы хотите сделать?', reply_markup=markup)
    elif message.text == 'Задать город проживания':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        city = message.text
        DataBase_manager.save_city(city)
        bot.send_message(message.chat.id, f"Ваш город '{city}' сохранен!")
        bot.reply_to(message,
                     'Введите город вашего проживания для того, чтобы мы могли каждый день присылать вам погоду🌍',
                     reply_markup=markup)
    elif message.text == 'Найти погоду в интересуещем городе':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        search_city = message.text
        temperature = ''
        bot.send_message(message.chat.id, f"Температура в городе {search_city}")


bot.polling()
