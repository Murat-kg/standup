import requests
import telebot
from threading import Thread
from time import sleep
import schedule
import keyboards as kb
from config import TOKEN


bot = telebot.TeleBot(TOKEN)


otchet = {}
otchet1 = {}
otchet2 = {}
otchet3 = {}
id_usersname = {}


@bot.message_handler(commands=['start', 'standup'])
def send_welcome(message):
    if message.chat.type == 'private':
        chat_id = str(message.chat.id)
        name = message.chat.first_name
        id_usersname.setdefault(chat_id, name)
        otchet.setdefault(name, {})
        otchet1.setdefault(name, {})
        otchet2.setdefault(name, {})
        otchet3.setdefault(name, {})
        msg = bot.send_message(chat_id, 'Добро пожаловать 👋\nВыберите группу в которой вы учитесь👨‍💻', reply_markup=kb.keyboard1)
        bot.register_next_step_handler(msg, change_standup)
    elif message.chat.type == 'supergroup' or message.chat.type == 'group':
        chat_id = message.chat.id
        bot.send_message(chat_id, f'Привет {message.from_user.first_name}, напиши мне в личку')


def change_standup(message):
    try:
        if message.chat.type == 'private':
            chat_id = str(message.chat.id)
            otchet3[message.chat.first_name] = message.text
            msg = bot.send_message(chat_id, 'Привет! Хотите пройти Stand Up?', reply_markup=kb.keyboard)
            bot.register_next_step_handler(msg, get_change)
        elif message.chat.type == 'supergroup' or message.chat.type == 'group':
            chat_id = message.chat.id
            bot.send_message(chat_id, f'Привет {message.from_user.first_name}, напиши мне в личку')
    except Exception as e:
        print(e)


def get_change(message):
    try:
        chat_id = message.chat.id
        if message.text == 'Да':
            msg = bot.send_message(chat_id, 'Хорошо! Что было сделано?')
            bot.register_next_step_handler(msg, get_to_do)
        else:
            msg = bot.send_message(chat_id, f'{message.chat.first_name}, не играйтесь!😠')
            bot.register_next_step_handler(msg, send_welcome)
    except Exception as e:
        print(e)


def start_get_done():
    try:
        for id in id_usersname.keys():
            msg = bot.send_message(id, f'Привет! Начнём StandUp.\nЧто вы сделали?')
            bot.register_next_step_handler(msg, get_to_do)
    except Exception as e:
        print(e)

def get_to_do(message):
    try:
        chat_id = message.chat.id
        otchet[message.chat.first_name] = message.text
        msg = bot.send_message(chat_id, f'{message.from_user.first_name}, какие у вас планы?')
        bot.register_next_step_handler(msg, get_problems)
    except Exception as e:
        print(e)


def get_problems(message):
    try:
        chat_id = message.chat.id
        otchet1[message.chat.first_name] = message.text
        msg = bot.send_message(chat_id, f'{message.from_user.first_name}, какие затруднения у вас возникли?')
        bot.register_next_step_handler(msg, get_bye)
        print(otchet1)
    except Exception as e:
        print(e)


def get_bye(message):
    try:
        chat_id = message.chat.id
        otchet2[message.chat.first_name] = message.text
        bot.send_message(chat_id, f'{message.from_user.first_name}, спасибо, что прошли StandUp😁')
        print(id_usersname)
        requests.post(url='http://34.64.233.41/api/add/', data={"group": otchet3.get(message.chat.first_name), \
                                                                  "user_name": message.chat.first_name, \
                                                                  "done": otchet.get(message.chat.first_name),\
                                                                  "todo": otchet1.get(message.chat.first_name),\
                                                                  "problems": otchet2.get(message.chat.first_name)})
    except Exception as e:
        print(e)



def schedule_():
    try:
        while True:
            schedule.run_pending()
            sleep(1)
    except Exception as e:
        print(e)

def function_to_run():
    for k, v in id_usersname.items():
        try:
            bot.send_message(k, '[' + v + '](tg://user?id=' + k + ') {ежедневный отчет} /standup', parse_mode='markdown')
        except Exception as e:
            bot.send_message(k, '[' + v + '](tg://user?id=' + k + ') ежедневный отчет /standup', parse_mode='markdown')

if __name__ == "__main__":
    schedule.every().day.at("10:10").do(function_to_run)
    Thread(target=schedule_).start()


bot.polling(none_stop=True, timeout=432000)
