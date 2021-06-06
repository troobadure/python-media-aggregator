from keyboards import keyboards
import time


def attach(bot, db_manager):
    @bot.message_handler(func=lambda message: message.text == 'add profile')
    def add_profile(message):
        user_name = message.from_user.full_name

        db_manager.update_state(user_name,
                            'main_menu',
                            time.strftime('%d/%m/%y, %X'),
                            message.chat.id)

        bot.send_message(message.chat.id,
                        'Выбери соцюшку сю',
                        reply_markup=keyboards.add_profile_inline_keyboard)

        print(user_name + ' at ' + db_manager.get_state(message.chat.id)[0])


    @bot.callback_query_handler(func=lambda call: call.data.startswith('add_'))
    def picking_inst_soc(call):

        if call.data.startswith('add_profile'):
            db_manager.update_state('🇫🇮🌲',
                                f"inserting{call.data[call.data.find('_')::]}",
                                time.strftime('%d/%m/%y, %X'),
                                call.message.chat.id)

            bot.send_message(call.message.chat.id,
                            f"Введи юзернейм профиля из {(call.data[call.data.find('_') + 9::]).capitalize()}",
                            reply_markup=keyboards.cancel_keyboard)

            print(db_manager.get_state(call.message.chat.id))


    # curr_state == inserting inst uname
    @bot.message_handler(func=lambda message: (db_manager.get_state(message.chat.id)).startswith('inserting_profile'))
    def inserting_inst_uname(message):

        if message.text == 'Охрана':
            db_manager.update_state('🇫🇮🌲',
                                'main_menu',
                                time.strftime('%d/%m/%y, %X'),
                                message.chat.id)
            bot.send_message(message.chat.id,
                            'Главное меню пева',
                            reply_markup=keyboards.main_menu_keyboard)

        else:
            bot.send_message(message.chat.id,
                            'РАЗРАБОТ',
                            reply_markup=keyboards.cancel_keyboard)
            db_manager.update_state('LOHs',
                                'inserting_instagram_us',
                                time.strftime('%d/%m/%y, %X'),
                                message.chat.id)