from keyboards import keyboards
import time


def attach(bot, db_manager):
    @bot.message_handler(func=lambda message: message.text == 'add criteria')
    def add_criteria(message):
        user_name = message.from_user.full_name

        db_manager.update_state(user_name,
                            'main_menu',
                            time.strftime('%d/%m/%y, %X'),
                            message.chat.id)

        bot.send_message(message.chat.id,
                        'Добавь креофанищью',
                        reply_markup=keyboards.add_criteria_inline_keyboard)