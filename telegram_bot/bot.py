import telebot
from config import config
from database import db_manager
from handlers import registration, add_profile, add_criteria, next_post, fetch_posts


# db_manager.init_db()
bot = telebot.TeleBot(config.BOT_TOKEN)


registration.attach(bot, db_manager)
add_profile.attach(bot, db_manager)
add_criteria.attach(bot, db_manager)
next_post.attach(bot, db_manager)
fetch_posts.attach(bot, db_manager)


bot.polling()
