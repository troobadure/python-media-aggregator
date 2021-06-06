from keyboards import keyboards
import time


def attach(bot, manager):
    @bot.message_handler(func=lambda message: message.text == 'add criteria')
    def add_criteria(message):
        user_name = message.from_user.first_name

        if message.from_user.last_name:
            user_name = f"{user_name} {message.from_user.last_name}"

        manager.update_state(user_name,
                            'main_menu',
                            time.strftime('%d/%m/%y, %X'),
                            message.chat.id)

        bot.send_message(message.chat.id,
                        'Добавь критерию',
                        reply_markup=keyboards.add_criteria_inline_keyboard)