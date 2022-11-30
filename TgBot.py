import requests
import random
import telebot
from bs4 import BeautifulSoup as b
from telebot import types

URL = 'https://wwv.zvuch.com/artists/%D0%B6%D1%89-134984'
YOUTUBE = 'https://y.com.sb/feed/popular'
API_KEY = '5725405963:AAEJNS2LOpDTF3iw9mFlRaPUKniOAsqNQow'


def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    songs = soup.find_all('li', class_='item')
    all_songs = [c.text for c in songs]
    clear_songs = []
    for x in all_songs:
        if x.count('ЖЩ') != 0:
            if x.count('(Обратно 2017)') != 0:
                clear_songs.append(x)
    return clear_songs


def charts(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    charts = soup.select('div > a > p[dir="auto"]')
    all_charts = [c.text for c in charts]
    clear_charts = []
    for i in range(0, 10, 2):
        clear_charts.append(all_charts[i])
    return clear_charts


list_of_charts = charts(YOUTUBE)
list_of_songs = parser(URL)
random.shuffle(list_of_songs)

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['YouTube'])
def start(message):
    mess = "В тренде сейчас:"
    bot.send_message(message.chat.id, mess, parse_mode='html')
    for i in range(5):
        print(bot.send_message(message.chat.id, list_of_charts[i]))


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name} {message.from_user.last_name}</b> !!! Ищите музыку по душе? Тогда тебе сюда,пишите "song", жмите любую цифру и наслаждайтесь :'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['website'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Посетить веб сайт", url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'))
    bot.send_message(message.chat.id, 'Не сдавайтесь', reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    website = types.KeyboardButton('/website')
    start = types.KeyboardButton('/help')
    markup.add(website, start)
    mess = "Возможные команды:\n" \
           "1) /help - получите данное сообщение;\n" \
           "2) /start - начальное сообщение;\n" \
           "3) song<N> вместо N подставьте любую цифру (если данная команда не работает, значит лимит доступных треков исчерпан;\n" \
           "4) Название песни - именно её имя без длинных отступов, ЖЩ и скобок с альбомом;\n" \
           "5) logo - получите невероятную картирнку;\n" \
           "6) Hello, Привет - фирменное приветствие\n" \
           "7) /YouTube - в тренде сейчас\n" \
           "8) Не забывайте про кнопки!"
    bot.send_message(message.chat.id, mess, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == 'Hello' or message.text == 'Привет':
        bot.send_message(message.chat.id, "привчёдел")
    elif message.text.lower() in ['song1', 'song2', 'song3', 'song4', 'song5', 'song6', 'song7', 'song8', 'song9']:
        bot.send_message(message.chat.id, list_of_songs[0])
        bot.send_message(message.chat.id, 'Хотите послушать? Введите название трека')
        del list_of_songs[0]
    elif message.text == "Боль всего мира":
        audio = open('Songs/ЖЩ - Обратно (2017)/1 - Боль всего мира.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)
    elif message.text == "Сломанное сердце":
        audio = open('Songs/ЖЩ - Обратно (2017)/2 - Сломанное сердце.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)
    elif message.text == "7000000000":
        audio = open('Songs/ЖЩ - Обратно (2017)/3 - 7000000000.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)
    elif message.text == "Гранж":
        audio = open('Songs/ЖЩ - Обратно (2017)/4 - Гранж.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)
    elif message.text == "Ключ":
        audio = open('Songs/ЖЩ - Обратно (2017)/5 - Ключ.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)
    elif message.text == "У меня есть мечта":
        audio = open('Songs/ЖЩ - Обратно (2017)/6 - У меня есть мечта.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)
    elif message.text == "Ты должен сдохнуть первым":
        audio = open('Songs/ЖЩ - Обратно (2017)/7 - Ты должен сдохнуть первым.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)
    elif message.text == "Впусти в себя добро":
        audio = open('Songs/ЖЩ - Обратно (2017)/8 - Впусти в себя добро.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)
    elif message.text == "Обратно":
        audio = open('Songs/ЖЩ - Обратно (2017)/9 - Обратно.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)
    elif message.text == "logo":
        photo = open("images/ZHSCH_logo.png", 'rb')
        bot.send_photo(message.chat.id, photo)

    else:
        bot.send_message(message.chat.id, "Don't understand you")


bot.polling()
