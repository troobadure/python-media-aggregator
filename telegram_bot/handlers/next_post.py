from keyboards import keyboards
import time


def attach(bot, db_manager):
    @bot.message_handler(func=lambda message: message.text == 'Наступна публікація' and db_manager.get_state(message.chat.id) == 'main_menu')
    def next_post(message):
        user_id = message.chat.id
        user_name = message.from_user.full_name

        db_manager.update_state(user_id,
                                user_name,
                                'main_menu',
                                time.strftime('%d/%m/%y, %X'))

        bot.send_message(user_id,
                        'Обробка публікації...',
                        reply_markup=keyboards.cancel_keyboard)


        video = open(
            "files/instagram/spacex_2021-05-18_20-27-38.mp4",
            'rb')

        bot.send_video(user_id, video, timeout=60, reply_markup=keyboards.main_menu_keyboard)
        bot.delete_message(user_id,
                            message.message_id + 1)
        video.close()