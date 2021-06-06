from keyboards import keyboards
import time


def attach(bot, db_manager):
    @bot.message_handler(func=lambda message: message.text == 'fetch posts')
    def fetch_posts(message):
        user_name = message.from_user.full_name

        db_manager.update_state(user_name,
                            'main_menu',
                            time.strftime('%d/%m/%y, %X'),
                            message.chat.id)

        bot.send_message(message.from_user.id,
                        '<b>(В РАЗРАПОПЕ)</b>',
                        reply_markup=keyboards.main_menu_keyboard,
                        parse_mode='HTML')