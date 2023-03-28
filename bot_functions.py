import os
import telebot
from stuff import *

token = os.environ.get('TELEGRAM_KEY')
bot = telebot.TeleBot(token)  # сам бот

answers = {
    'help': '''Введи запрос для поиска в формате 
    <i>"GIT запрос язык_программирования"</i> 
    и я дам тебе список ссылок.'''
}


@bot.message_handler(commands=['start', 'help', 'dog'])
def start(message):  # параметр - это сообщение от пользователя
    if message.text == '/start':
        bot.send_message(message.chat.id, f"Hello, {message.chat.username}!👋")
    elif message.text == '/help':
        bot.send_message(message.chat.id, text=answers['help'], parse_mode='html')
    elif message.text == '/dog':
        img = send_image()
        bot.send_photo(message.chat.id, photo=img)


@bot.message_handler(commands=['buttons'])
def button_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Поделиться номером телефона', request_contact=True)
    btn2 = telebot.types.KeyboardButton('Поделиться локацией', request_location=True)
    markup.add(btn1)
    markup.add(btn2)
    bot.send_message(message.chat.id, 'Выбери кнопку', reply_markup=markup)


@bot.message_handler(content_types=['contact', 'location'])
def save_user(message):
    if message.contact is not None:  # если номер телефона передали
        with open('users.txt', 'a', encoding='utf-8') as file:  # записываем инфу о пользователе в файл
            file.write(f'{message.contact}\n')
    elif message.location is not None:  # если локацию передали
        city = get_city(message.location.latitude, message.location.longitude)
        bot.send_message(message.chat.id, str(city))


@bot.message_handler(content_types=['text'])  # эта функция обрабатывает текст
def text_messages(message):
    if message.text.startswith('GIT'):  # если текст сообщения начинается с букв GIT
        msg = message.text.split()  # разбиваем сообщение на список
        res = git_search(msg[1], msg[2])  # ['GIT', 'requests', 'python']
        ans = "Вот, что я нашел:\n" + res   # объединяем список репозиториев с текстом
        bot.send_message(message.chat.id, text=ans, parse_mode='html')