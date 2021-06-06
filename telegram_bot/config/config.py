import os

DATABASE_STRING = os.getenv('DATABASE_STRING')
if not DATABASE_STRING:
    print('You have not set DATABASE_STRING')
    quit()    

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    print('You have not set BOT_TOKEN')
    quit()
