import os
import telebot
from stuff import *

token = os.environ.get('TELEGRAM_KEY')
bot = telebot.TeleBot(token)  # сам бот



@bot.message_handler(commands=['start', 'help', 'dog'])
def start(message):  # параметр - это сообщение от пользователя
    if message.text == '/start':
        user = message.chat.username
        template = make_tamplate('templates/start.html')
        msg = template.render(username=user)
        bot.send_message(message.chat.id, msg, parse_mode='html')
    elif message.text == '/help':
        template = make_tamplate('templates/start.html')
        msg = template.render()
        bot.send_message(message.chat.id, msg, parse_mode='html')
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
    if message.contact is not None:
        connect = connect_db()
        cont = message.contact
        u = add_user(cont.first_name, cont.last_name, cont.user_id, cont.phone_number, connect)# если номер телефона передали
        if u is not None:
            bot.send_message(message.chat.id, 'Спасибо, но дату  воей смерти было бы приятней увидеть ХО')
        else:
            bot.send_message(message.chat.id, 'Лох, ты это уже кидал')
    elif message.location is not None:  # если локацию передали
        lat = message.location.latitude
        lon = message.location.longitude
        forecast = get_forecast(lat, lon)
        bot.send_message(message.chat.id, text=forecast, parse_mode='html')


@bot.message_handler(content_types=['text'])  # эта функция обрабатывает текст
def text_messages(message):
    if message.text.startswith('GIT'):  # если текст сообщения начинается с букв GIT
        msg = message.text.split()  # разбиваем сообщение на список
        res = git_search(msg[1], msg[2])  # ['GIT', 'requests', 'python']
        ans = "Вот, что я нашел:\n" + res   # объединяем список репозиториев с текстом
        bot.send_message(message.chat.id, text=ans, parse_mode='html')