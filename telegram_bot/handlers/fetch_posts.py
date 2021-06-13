from keyboards import keyboards
import time
from loaders import instagram_loader


def attach(bot, db_manager):
    @bot.message_handler(func=lambda message: message.text == 'Завантажити публікації' and db_manager.get_state(message.chat.id) == 'main_menu')
    def fetch_posts(message):
        user_id = message.chat.id
        user_name = message.from_user.full_name

        db_manager.update_state(user_id,
                                user_name,
                                'main_menu',
                                time.strftime('%d/%m/%y, %X'))

        bot.send_message(user_id,
                        '<i>Завантаження публікацій розпочато</i>',
                        reply_markup=keyboards.cancel_keyboard,
                        parse_mode='HTML')

        profiles = db_manager.get_profiles(user_id)
        for profile in profiles:
            if profile.profile_type == 'instagram':
                likes_percentage = db_manager.get_criteria_value(profile.profile_id, 'likesviews')
                instagram_loader.load_profile(profile.profile_name, likes_percentage, 30)

        bot.send_message(user_id,
                        '<i>Завантаження публікацій завершено</i>',
                        reply_markup=keyboards.main_menu_keyboard,
                        parse_mode='HTML')