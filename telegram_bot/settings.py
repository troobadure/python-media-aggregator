import os


BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
if not BOT_TOKEN:
    print('You have not set BOT_TOKEN')
    quit()

# HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')


# WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
# WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
# WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'


# WEBAPP_HOST = '0.0.0.0'
# WEBAPP_PORT = int(os.getenv('PORT'))
