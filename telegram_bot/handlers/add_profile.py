from keyboards import keyboards
import time


profile_type = 'initial type'

def attach(bot, db_manager):
    @bot.message_handler(func=lambda message: message.text == 'Add profile' and db_manager.get_state(message.chat.id) == 'main_menu')
    def add_profile(message):
        user_id = message.chat.id
        user_name = message.from_user.full_name

        db_manager.update_state(user_id,
                                user_name,
                                'add_profile_type',
                                time.strftime('%d/%m/%y, %X'))
                                
        bot.send_message(user_id,
                        'Выбери сосюцюшку',
                        reply_markup=keyboards.select_profile_type_inline_keyboard)


    @bot.callback_query_handler(func=lambda call: call.data.startswith('select_profile_') and db_manager.get_state(call.message.chat.id) == 'add_profile_type')
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


    @bot.message_handler(func=lambda message: message.text != 'Охрана' and db_manager.get_state(message.chat.id) == 'add_profile_name')
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
