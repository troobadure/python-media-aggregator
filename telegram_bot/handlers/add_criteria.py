from keyboards import keyboards
import time


criteria_profile_type = 'initial type crit'
criteria_profile_name = 'initial name crit'
criteria_type = 'initial criteria type'

def attach(bot, db_manager):
    @bot.message_handler(func=lambda message: message.text == 'Додати критерій' and db_manager.get_state(message.chat.id) == 'main_menu')
    def add_criteria(message):
        user_id = message.chat.id
        user_name = message.from_user.full_name

        db_manager.update_state(user_id,
                                user_name,
                                'add_criteria_profile_type',
                                time.strftime('%d/%m/%y, %X'))
                                
        bot.send_message(user_id,
                        'Оберіть соціальну мережу',
                        reply_markup=keyboards.select_profile_type_inline_keyboard)


    @bot.callback_query_handler(func=lambda call: call.data.startswith('select_profile_') and db_manager.get_state(call.message.chat.id) == 'add_criteria_profile_type')
    def add_criteria_profile_type(call):
        global criteria_profile_type 

        user_id = call.message.chat.id
        user_name = call.message.from_user.full_name
        criteria_profile_type = call.data.split('select_profile_')[1]

        db_manager.update_state(user_id,
                                user_name,
                                'add_criteria_profile_name',
                                time.strftime('%d/%m/%y, %X'))

        bot.send_message(user_id,
                        f"Введіть назву профілю з {(call.data.split('select_profile_')[1]).capitalize()}",
                        reply_markup=keyboards.cancel_keyboard)


    @bot.message_handler(func=lambda message: message.text != 'Відміна' and db_manager.get_state(message.chat.id) == 'add_criteria_profile_name')
    def add_criteria_profile_name(message):
        global criteria_profile_type, criteria_profile_name

        user_id = message.chat.id
        user_name = message.from_user.full_name
        criteria_profile_name = message.text

        db_manager.update_state(user_id,
                            user_name,
                            'add_criteria_type',
                            time.strftime('%d/%m/%y, %X'))

        bot.send_message(user_id,
                        'Профіль знайдено. Оберіть тип критерію',
                        reply_markup=keyboards.select_criteria_type_inline_keyboard)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('select_criteria_') and db_manager.get_state(call.message.chat.id) == 'add_criteria_type')
    def add_criteria_type(call):
        global criteria_profile_type, criteria_profile_name, criteria_type

        user_id = call.message.chat.id
        user_name = call.message.from_user.full_name
        criteria_type = call.data.split('select_criteria_')[1]

        db_manager.update_state(user_id,
                                user_name,
                                'add_criteria_name',
                                time.strftime('%d/%m/%y, %X'))

        bot.send_message(user_id,
                        f"Введіть значення критерію",
                        reply_markup=keyboards.cancel_keyboard)


    @bot.message_handler(func=lambda message: message.text != 'Відміна' and db_manager.get_state(message.chat.id) == 'add_criteria_name')
    def add_criteria_name(message):
        global criteria_profile_type, criteria_profile_name, criteria_type

        user_id = message.chat.id
        user_name = message.from_user.full_name
        criteria_name = message.text

        db_manager.update_state(user_id,
                                user_name,
                                'main_menu',
                                time.strftime('%d/%m/%y, %X'))

        criteria_profile_id = db_manager.get_profile_id(user_id, criteria_profile_type, criteria_profile_name)

        db_manager.insert_criteria(criteria_profile_id,
                                    criteria_type,
                                    criteria_name)

        bot.send_message(user_id,
                        'Критерій додано',
                        reply_markup=keyboards.main_menu_keyboard)
