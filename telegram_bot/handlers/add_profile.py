from keyboards import keyboards
import time


profile_type = 'initial type'

def attach(bot, db_manager):
    @bot.message_handler(func=lambda message: message.text == 'Додати профіль' and db_manager.get_state(message.chat.id) == 'main_menu')
    def add_profile(message):
        user_id = message.chat.id
        user_name = message.from_user.full_name

        db_manager.update_state(user_id,
                                user_name,
                                'add_profile_type',
                                time.strftime('%Y-%m-%d %X'))
                                
        bot.send_message(user_id,
                        'Оберіть соціальну мережу',
                        reply_markup=keyboards.select_profile_type_inline_keyboard)


    @bot.callback_query_handler(func=lambda call: call.data.startswith('select_profile_') and db_manager.get_state(call.message.chat.id) == 'add_profile_type')
    def add_profile_type(call):
        global profile_type 

        user_id = call.message.chat.id
        user_name = call.message.from_user.full_name
        profile_type = call.data.split('select_profile_')[1]

        db_manager.update_state(user_id,
                                user_name,
                                'add_profile_name',
                                time.strftime('%Y-%m-%d %X'))

        bot.send_message(user_id,
                        f"Введіть назву профілю {(call.data.split('select_profile_')[1]).capitalize()}",
                        reply_markup=keyboards.cancel_keyboard)


    @bot.message_handler(func=lambda message: message.text != 'Відміна' and db_manager.get_state(message.chat.id) == 'add_profile_name')
    def add_profile_name(message):
        global profile_type

        user_id = message.chat.id
        user_name = message.from_user.full_name
        profile_name = message.text

        db_manager.update_state(user_id,
                            user_name,
                            'main_menu',
                            time.strftime('%Y-%m-%d %X'))

        db_manager.insert_profile(user_id,
                                profile_type,
                                profile_name)

        bot.send_message(user_id,
                        'Профіль додано',
                        reply_markup=keyboards.main_menu_keyboard)
