import telebot
import glob
import json
import os
import psycopg2
import config.config_heroku
from loader import main

# DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL, sslmode='require')     

# BOT_TOKEN = os.getenv('BOT_TOKEN')
# DATABASE_URL = os.getenv('DATABASE_URL')
# if not BOT_TOKEN:
#     print('You have not set BOT_TOKEN')
#     quit()
bot = telebot.TeleBot(BOT_TOKEN)

skipped = 0

currentProfile = ''
settingLikes = False

@bot.message_handler(commands = ['get_post'])
def get_post(message):
    cursor = conn.cursor()
    try:
        sql_insert = 'INSERT INTO public.users (id) VALUES (\'%s\'::character varying);'
        cursor.execute(sql_insert % (message.from_user.username))
        conn.commit()
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()
    check_owner(message)
    global skipped
    bot.send_chat_action(message.chat.id, 'typing')

    filename = glob.glob('telegram_bot/db_proto/content/*.mp4')[0]
    video = open(filename, 'rb')
    bot.send_video(message.chat.id, video)
    skipped += 1

@bot.message_handler(commands = ['add_profile'])
def add_profile(message):
    check_owner(message)
    bot.send_chat_action(message.chat.id, 'typing')

    with open('telegram_bot/db_proto/profiles.json', 'r') as jsonFile:
        data = json.load(jsonFile)
        data['profiles'].append({'name': message.text.split()[1], 'likes': 0})

    with open('telegram_bot/db_proto/profiles.json', 'w') as jsonFile:
        json.dump(data, jsonFile)

    bot.reply_to(message, '*profile added*')
    

@bot.message_handler(commands = ['remove_profile'])
def remove_profile(message):
    check_owner(message)
    bot.send_chat_action(message.chat.id, 'typing')

    found = False
    with open('telegram_bot/db_proto/profiles.json', 'r') as jsonFile:
        data = json.load(jsonFile)         
        for i in range(len(data['profiles'])):
            if data['profiles'][i]['name'] == message.text.split()[1]:
                found = True
                data['profiles'].pop(i)
                break
        
    if found:
        with open('telegram_bot/db_proto/profiles.json', 'w') as jsonFile:
            json.dump(data, jsonFile)

        bot.reply_to(message, '*profile removed*')
    else:
        bot.reply_to(message, '*profile not found*')

@bot.message_handler(commands = ['set_likes'])
def set_likes(message):
    global settingLikes
    check_owner(message)
    bot.send_chat_action(message.chat.id, 'typing')
    settingLikes = True
    bot.reply_to(message, '*write the profile name*')

@bot.message_handler(commands = ['fetch_posts'])
def fetch_posts(message):
    check_owner(message)
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message, '*starting fetch*')
    main()
    bot.reply_to(message, '*finishing fetch*')

@bot.message_handler()
def test_message_handler(message):
    global settingLikes, currentProfile
    check_owner(message)
    if settingLikes:
        if message.text == '':
            settingLikes = False
            currentProfile = False
            bot.reply_to(message, 'input cannot be empty')
            exit()

        if currentProfile == '':
            currentProfile = message.text
            bot.reply_to(message, 'write likes')
        else:
            found = False
            with open('telegram_bot/db_proto/profiles.json', 'r') as jsonFile:
                data = json.load(jsonFile)
                for profile in data['profiles']:
                    if (profile["name"] == currentProfile):
                        found = True
                        profile["likes"] = message.text
                        break
            
            settingLikes = False
            currentProfile = False
            if found:
                with open('telegram_bot/db_proto/profiles.json', 'w') as jsonFile:
                    json.dump(data, jsonFile)

                bot.reply_to(message, 'likes set')
            else:
                bot.reply_to(message, 'profile not found')
    else:
        bot.reply_to(message, 'message_handler invoked')




def check_owner(message):
    if message.from_user.username != 'troobadure':
        warning = ('!!!STRANGER DETECTED!!!\n'
        'username={0} chat_id={1}').format(message.chat.username, message.chat.id)
        print(warning)
        bot.send_message('402027899', warning)
        bot.stop_polling()
        exit()


bot.polling(none_stop = True)