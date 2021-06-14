from keyboards import keyboards
import time


def attach(bot, db_manager):
    @bot.message_handler(commands=['start', 'START'])
    def start_command(message):
        user_id = message.chat.id
        user_name = message.from_user.full_name

        db_manager.insert_user(user_id,
                                user_name,
                                'main_menu',
                                time.strftime('%Y-%m-%d %X'),
                                time.strftime('%Y-%m-%d %X'))

        bot.send_message(user_id,
                        f"Вітаю, {user_name}!",
                        reply_markup=keyboards.main_menu_keyboard)
