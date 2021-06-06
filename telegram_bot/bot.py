import telebot
from config import config
from database import manager
from loaders.loader import main
from handlers import registration, add_profile, add_criteria, get_post, fetch_posts


manager.init_db()
bot = telebot.TeleBot(config.BOT_TOKEN)


registration.attach(bot, manager)
add_profile.attach(bot, manager)
add_criteria.attach(bot, manager)
get_post.attach(bot, manager)
fetch_posts.attach(bot, manager)


bot.polling()
