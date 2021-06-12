from keyboards import keyboards
import time


profile_type = 'initial type'

def attach(bot, db_manager):
    @bot.message_handler(func=lambda message: message.text == 'add profile')
    def add_profile(message):
        user_id = message.chat.id
        user_name = message.from_user.full_name

        db_manager.update_state(user_id,
                                user_name,
                                'add_profile_type',
                                time.strftime('%d/%m/%y, %X'))
                                
        bot.send_message(user_id,
                        'Выбери сосюцюшку',
                        reply_markup=keyboards.add_profile_inline_keyboard)


    @bot.callback_query_handler(func=lambda call: call.data.startswith('add_profile'))
    def add_profile_type(call):
        global profile_type 

        user_id = call.message.chat.id
        user_name = call.message.from_user.full_name
        profile_type = call.data[call.data.find('_') + 9::]

        db_manager.update_state(user_id,
                                user_name,
                                'add_profile_name',
                                time.strftime('%d/%m/%y, %X'))

        bot.send_message(user_id,
                        f"Введи юзерkek профile из {(call.data[call.data.find('_') + 9::]).capitalize()}",
                        reply_markup=keyboards.cancel_keyboard)


    @bot.message_handler(func=lambda message: db_manager.get_state(message.chat.id) == 'add_profile_name' and message.text != 'Охрана')
    def add_profile_name(message):
        global profile_type

        user_id = message.chat.id
        user_name = message.from_user.full_name
        profile_name = message.text

        db_manager.update_state(user_id,
                            user_name,
                            'main_menu',
                            time.strftime('%d/%m/%y, %X'))

        db_manager.insert_profile(user_id,
                                profile_type,
                                profile_name)

        bot.send_message(user_id,
                        'Профуль запечатано',
                        reply_markup=keyboards.main_menu_keyboard)
