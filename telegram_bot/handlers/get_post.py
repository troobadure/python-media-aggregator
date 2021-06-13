from keyboards import keyboards
import time


def attach(bot, db_manager):
    @bot.message_handler(func=lambda message: message.text == 'Get post')
    def get_post(message):
        user_name = message.from_user.full_name

        db_manager.update_state(user_name,
                            'main_menu',
                            time.strftime('%d/%m/%y, %X'),
                            message.chat.id)

        video = open(
            "/home/leap_sunrise/python-media-aggregatorq/telegram_bot/db_proto/content/_score_shadowguy.__2020-10-04_14-38-25_1.mp4",
            'rb')
        bot.send_message(message.chat.id,
                        'Видео обраебатывается...',
                        reply_markup=keyboards.main_menu_keyboard)

        bot.send_video(message.chat.id, video, timeout=60, reply_markup=keyboards.main_menu_keyboard)
        bot.delete_message(message.chat.id,
                        message.message_id + 1)
        video.close()