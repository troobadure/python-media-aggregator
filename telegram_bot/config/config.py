import os

DATABASE_STRING = "dbname=postgres user=postgres host=localhost password=1111 port=5432"
if not DATABASE_STRING:
    print('You have not set DATABASE_PARAM')
    quit()    

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    print('You have not set BOT_TOKEN')
    quit()
