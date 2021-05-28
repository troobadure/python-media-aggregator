import os

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    print('You have not set DATABASE_URL')
    quit()    

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    print('You have not set BOT_TOKEN')
    quit()
