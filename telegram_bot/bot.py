import telebot
from keyboards import keyboards
from db import dbmanager
from loaders.loader import main
import time
from config.config import BOT_TOKEN


bot = telebot.TeleBot(BOT_TOKEN)
dbmanager.init_db()

@bot.message_handler(commands=['start', 'START'])
def start_message(message):
    user_name = message.from_user.first_name

    if message.from_user.last_name:
        user_name = f"{user_name} {message.from_user.last_name}"

    bot.send_message(message.chat.id,
                     f"Hellol, {user_name}",
                     reply_markup=keyboards.main_menu_keyboard)

    dbmanager.register_user(message.chat.id,
                            user_name,
                            'main_menu',
                            time.strftime('%d/%m/%y, %X'),
                            time.strftime('%d/%m/%y, %X'))


@bot.message_handler(func=lambda message: message.text == 'fetch posts')
def fetch_posts(message):
    user_name = message.from_user.first_name

    if message.from_user.last_name:
        user_name = f"{user_name} {message.from_user.last_name}"

    dbmanager.update_state(user_name,
                           'main_menu',
                           time.strftime('%d/%m/%y, %X'),
                           message.chat.id)

    bot.send_message(message.from_user.id,
                     '<b>(В РАЗРАБОТКЕ)</b>',
                     reply_markup=keyboards.main_menu_keyboard,
                     parse_mode='HTML')


@bot.message_handler(func=lambda message: message.text == 'get post')
def get_post(message):
    user_name = message.from_user.first_name

    if message.from_user.last_name:
        user_name = f"{user_name} {message.from_user.last_name}"

    dbmanager.update_state(user_name,
                           'main_menu',
                           time.strftime('%d/%m/%y, %X'),
                           message.chat.id)

    video = open(
        "/home/leap_sunrise/python-media-aggregatorq/telegram_bot/db_proto/content/_score_shadowguy.__2020-10-04_14-38-25_1.mp4",
        'rb')
    bot.send_message(message.chat.id,
                     'Видео обрабатывается...',
                     reply_markup=keyboards.main_menu_keyboard)

    bot.send_video(message.chat.id, video, timeout=60, reply_markup=keyboards.main_menu_keyboard)
    bot.delete_message(message.chat.id,
                       message.message_id + 1)
    video.close()


@bot.message_handler(func=lambda message: message.text == 'add profile')
def add_profile(message):
    user_name = message.from_user.first_name

    if message.from_user.last_name:
        user_name = f"{user_name} {message.from_user.last_name}"

    dbmanager.update_state(user_name,
                           'main_menu',
                           time.strftime('%d/%m/%y, %X'),
                           message.chat.id)

    bot.send_message(message.chat.id,
                     'Выбери соц. сеть',
                     reply_markup=keyboards.add_profile_inline_keyboard)

    print(dbmanager.get_state(message.chat.id)[0])


@bot.message_handler(func=lambda message: message.text == 'add criteria')
def add_criteria(message):
    user_name = message.from_user.first_name

    if message.from_user.last_name:
        user_name = f"{user_name} {message.from_user.last_name}"

    dbmanager.update_state(user_name,
                           'main_menu',
                           time.strftime('%d/%m/%y, %X'),
                           message.chat.id)

    bot.send_message(message.chat.id,
                     'Добавь критерию',
                     reply_markup=keyboards.add_criteria_inline_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('add_'))
def picking_inst_soc(call):

    if call.data.startswith('add_profile'):
        dbmanager.update_state('🇫🇮🌲',
                               f"inserting{call.data[call.data.find('_')::]}",
                               time.strftime('%d/%m/%y, %X'),
                               call.message.chat.id)

        bot.send_message(call.message.chat.id,
                         f"Введи юзернейм профиля из {(call.data[call.data.find('_') + 9::]).capitalize()}",
                         reply_markup=keyboards.cancel_keyboard)

        print(dbmanager.get_state(call.message.chat.id))


# curr_state == inserting inst uname
@bot.message_handler(func=lambda message: (dbmanager.get_state(message.chat.id)).startswith('inserting_profile'))
def inserting_inst_uname(message):

    if message.text == 'Отмена':
        dbmanager.update_state('🇫🇮🌲',
                               'main_menu',
                               time.strftime('%d/%m/%y, %X'),
                               message.chat.id)
        bot.send_message(message.chat.id,
                         'Главное меню',
                         reply_markup=keyboards.main_menu_keyboard)

    else:
        bot.send_message(message.chat.id,
                         'В РАЗРАБОТКЕ',
                         reply_markup=keyboards.cancel_keyboard)
        dbmanager.update_state('LOH',
                               'inserting_instagram_us',
                               time.strftime('%d/%m/%y, %X'),
                               message.chat.id)



bot.polling()
