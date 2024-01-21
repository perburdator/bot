import json

import telebot
from telebot import types

from informat import help_text, about_text, first_loc_photo, photo_loc_3, photo_loc_1, photo_loc_2, photo_loc_11, \
    photo_loc_12, photo_loc_122, photo_loc_21, photo_loc_22, secret_text

token = "6720101690:AAEMfduKLaTCrls53RPDW4xAwDvOZB8KJzI"  # токен моего тест-бота с очень оригинальным айди

bot = telebot.TeleBot(token=token)

filename = "userdata.json"


# Хэндлеры для обработки мн-ва сообщений
@bot.message_handler(content_types=["video"])
def video_func(message):
    bot.reply_to(message, text="Этот контент не поддерживается ботом. \n"
                               "Нажмите /start для перезапуска"
                 )


@bot.message_handler(content_types=["photo"])
def photo_func(message):
    bot.reply_to(message, text="Этот контент не поддерживается ботом. \n"
                               "Нажмите /start для перезапуска"
                 )


@bot.message_handler(content_types=["animation"])
def animation_func(message):
    bot.reply_to(message, text="Этот контент не поддерживается ботом. \n"
                               "Нажмите /start для перезапуска"
                 )


@bot.message_handler(content_types=["audio"])
def audio_func(message):
    bot.reply_to(message, text="Этот контент не поддерживается ботом. \n"
                               "Нажмите /start для перезапуска"
                 )


@bot.message_handler(content_types=["sticker"])
def sticker_func(message):
    bot.reply_to(message, text="Этот контент не поддерживается ботом. \n"
                               "Нажмите /start для перезапуска")


# Считываем дату с геймдаты
def load_data():
    try:
        with open('gamedata.json', 'r', encoding='utf8') as f:
            dataset = json.load(f)
    except FileNotFoundError:
        dataset = {}

    return dataset


# Объявление "даты"
data = load_data()
game_data = data['game_data']
# Некий костыль для прочтения и записи данных от пользователя в юзердату
def read_data():
    try:
        with open('userdata.json', 'r', encoding='utf8') as f:
            dataset = json.load(f)
    except FileNotFoundError:
        dataset = {}

    return dataset


userdata = read_data()


def save_data(userdata):
    with open(filename, "w") as f:
        json.dump(userdata, f)


# Хэндлер про зачем грубо говоря существует бот
@bot.message_handler(commands=['about'])
def about_func(message):
    user = message.chat.id
    bot.send_message(user, text=about_text)


# Хэндлер помощи
@bot.message_handler(commands=['help'])
def help_func(message):
    user = message.chat.id
    bot.send_message(user, text=help_text)
@bot.message_handler(commands=['idkfa'])
def secret_message(message):
    user_id = message.chat.id
    if message.text == '/idkfa':
        bot.send_message(user_id, secret_text)
# Основной хендлер + начало
@bot.message_handler(commands=['start'])
def start_func(message):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    # создание и добавление кнопок на созданную клавиатуру
    button1 = types.KeyboardButton(text='Да')
    button2 = types.KeyboardButton(text='Нет')
    keyboard.add(button1, button2)

    bot.send_message(message.chat.id, "Вы находитесь на абсурд-квесте в телеграмм(Для справки /help). Вы готовы начать?", reply_markup=keyboard)
    save_data(data)  # сохранение инфы пользователя
    # отправление пользователю сообщения

# Функция запустится, когда пользователь нажмет на кнопку Да или Нет
@bot.message_handler(content_types=['text'])
def starting(message):
    user_id = message.chat.id
    if message.text == 'Нет':
        bot.send_message(user_id, text='Хорошо, когда захочешь пройти тест просто нажми на /start')
    elif message.text == 'Да':
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        but1 = types.KeyboardButton(game_data['starting']['but1'])
        but2 = types.KeyboardButton(game_data['starting']['but2'])
        but3 = types.KeyboardButton(game_data['starting']['but3'])
        keyboard.add(but1, but2, but3)
        bot.send_message(user_id, text=game_data['starting']['description'].format(message.from_user),
                         reply_markup=keyboard)
        bot.send_photo(user_id, photo=first_loc_photo)
        bot.register_next_step_handler_by_chat_id(user_id, loc)
        save_data(data)
    else:  # обработка непредвиденного рез-а
        bot.send_message(user_id, text='Я вас не понял до конца. Напишите /start для перезапуска.')


# Развилки сюжета
def loc(message):
    user_id = message.chat.id
    # 3 развилка и глупый финал
    if message.text == game_data['starting']['but3']:
        bot.send_photo(user_id, photo_loc_3)
        bot.send_message(user_id, text=game_data['loc3']['description'])
        bot.send_message(user_id, text="Для перезапуска напишите /start")
    # 1 развилка и создание кнопок её веток
    elif message.text == game_data['starting']['but1']:
        bot.send_photo(user_id, photo_loc_1)
        bot.send_message(user_id, text=game_data['location1']['description'])
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        choice1 = types.KeyboardButton(game_data['location1']['but1'])
        choice2 = types.KeyboardButton(game_data['location1']['but2'])
        keyboard.add(choice1, choice2)
        bot.send_message(message.chat.id, "Выберите действие ", reply_markup=keyboard)
        bot.register_next_step_handler_by_chat_id(user_id, loc1)
        save_data(data)
    # 2 развилка и создание кнопок её веток
    elif message.text == game_data['starting']['but2']:
        bot.send_photo(user_id, photo_loc_2)
        bot.send_message(user_id, text=game_data['location2']['description'])
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        choice1 = types.KeyboardButton(game_data['location2']['but1'])
        choice2 = types.KeyboardButton(game_data['location2']['but2'])
        keyboard.add(choice1, choice2)
        bot.send_message(message.chat.id, "Выберите действие :", reply_markup=keyboard)
        bot.register_next_step_handler_by_chat_id(user_id, loc1)
        save_data(data)
    # bot.send_photo(user_id, game_data['loc2']['photo_loc_2']) 2

# Вывод выбранной концовки и их финалы
def loc1(message):
    user_id = message.chat.id
    if message.text == game_data['location1']['but1']:
        bot.send_photo(user_id, photo_loc_11)
        bot.send_message(user_id, text=game_data['loc11']['description'])
        bot.send_message(user_id, text=game_data['loc11']['finale'])  # плохой финал
        bot.send_message(user_id, text="Для перезапуска напишите /start")
        save_data(data)
    elif message.text == game_data['location1']['but2']:
        bot.send_photo(user_id, photo_loc_12)
        bot.send_photo(user_id, photo_loc_122)
        bot.send_message(user_id, text=game_data['loc12']['description'])
        bot.send_message(user_id, text=game_data['loc12']['finale'])  # единственный финал, где гг жив
        bot.send_message(user_id, text="Возможно есть здесь секрет?")
        bot.register_next_step_handler_by_chat_id(user_id, secret_text)
        bot.send_message(user_id, text="Для перезапуска напишите /start")
        save_data(data)
    elif message.text == game_data['location2']['but1']:
        bot.send_photo(user_id, photo_loc_21)
        bot.send_message(user_id, text=game_data['loc21']['description'])
        bot.send_message(user_id, text=game_data['loc21']['finale'])  # плохой финал
        bot.send_message(user_id, text="Для перезапуска напишите /start")
        save_data(data)
    elif message.text == game_data['location2']['but2']:
        bot.send_photo(user_id, photo_loc_22)
        bot.send_message(user_id, text=game_data['loc22']['description'])
        bot.send_message(user_id, text=game_data['loc22']['finale'])  # плохой финал
        bot.send_message(user_id, text="Для перезапуска напишите /start")
        save_data(data)



bot.infinity_polling()  # Запуск бота

# вот такой, уже не простенький бот....
