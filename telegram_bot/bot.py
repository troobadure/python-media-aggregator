import logging

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling, start_webhook
from settings import (BOT_TOKEN, DATABASE_URL)

# ,
                        #   WEBHOOK_URL, WEBHOOK_PATH,
                        #   WEBAPP_HOST, WEBAPP_PORT

import psycopg2


conn = psycopg2.connect(DATABASE_URL, sslmode='require')     

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler()
async def echo(message: types.Message):
    logging.warning(f'Recieved a message from {message.from_user}')
    cursor = conn.cursor()
    try:
        sql_insert = 'INSERT INTO public.users (user_id) VALUES (\'%s\'::character varying);'
        cursor.execute(sql_insert % (message.from_user.username))
        conn.commit()
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()
    await bot.send_message(message.chat.id, 'Wat do u mean ' + message.text)


# @dp.message_handler(commands = ['add_profile'])
# async def add_profile(message):
#     await check_owner(message)
#     await bot.send_chat_action(message.chat.id, 'typing')

#     with open('telegram_bot/db_proto/profiles.json', 'r') as jsonFile:
#         data = json.load(jsonFile)
#         data['profiles'].append({'name': message.text.split()[1], 'likes': 0})

#     with open('telegram_bot/db_proto/profiles.json', 'w') as jsonFile:
#         json.dump(data, jsonFile)

#     await bot.send_message(message.chat.id, '*profile added*')


# async def check_owner(message):
#     if message.from_user.username != 'troobadure2':
#         warning = ('!!!STRANGER DETECTED!!!\n'
#         'username={0} chat_id={1}').format(message.chat.username, message.chat.id)
#         print(warning)
#         await bot.send_message('402027899', warning)


# async def on_startup(dp):
#     logging.warning(
#         'Starting webhook connection.')
#     await bot.set_webhook(WEBHOOK_URL,drop_pending_updates=True)


# async def on_shutdown(dp):
#     logging.warning('Shutting down webhook connection')


# def main():
#     logging.basicConfig(level=logging.INFO)
#     start_webhook(
#         dispatcher=dp,
#         webhook_path=WEBHOOK_PATH,
#         skip_updates=True,
#         on_startup=on_startup,
#         host=WEBAPP_HOST,
#         port=WEBAPP_PORT,
#     )

if __name__ == '__main__':
    start_polling(dp)
