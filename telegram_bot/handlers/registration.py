from keyboards import keyboards
import time


def attach(bot, manager):
    @bot.message_handler(commands=['start', 'START'])
    def start_message(message):
        user_name = message.from_user.first_name

        if message.from_user.last_name:
            user_name = f"{user_name} {message.from_user.last_name}"

        bot.send_message(message.chat.id,
                        f"Hellol, {user_name}",
                        reply_markup=keyboards.main_menu_keyboard)

        manager.register_user(message.chat.id,
                                user_name,
                                'main_menu',
                                time.strftime('%d/%m/%y, %X'),
                                time.strftime('%d/%m/%y, %X'))