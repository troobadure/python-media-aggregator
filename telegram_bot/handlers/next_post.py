from keyboards import keyboards
import time, os


def attach(bot, db_manager):
    @bot.message_handler(func=lambda message: message.text == 'Наступна публікація' and db_manager.get_state(message.chat.id) == 'main_menu')
    def next_post(message):
        user_id = message.chat.id
        user_name = message.from_user.full_name

        db_manager.update_state(user_id,
                                user_name,
                                'main_menu',
                                time.strftime('%Y-%m-%d %X'))

        bot.send_message(user_id,
                        'Надсилається...',
                        reply_markup=keyboards.cancel_keyboard)

        last_post = db_manager.get_last_post();
        
        if last_post == 0:
            bot.send_message(user_id,
                            'Ви переглянули всі завантажені публікації',
                            reply_markup=keyboards.main_menu_keyboard,
                            parse_mode='HTML')
            exit()

        file_pattern = 'files/' + last_post.profile_type + '/' + last_post.filename
        post_text = last_post.profile_type + ' <b>' + last_post.profile_name + '</b> - ' + last_post.publication_date
        with open(file_pattern + '.txt') as f:
            post_text += '\n' + f.read()

        for f in os.listdir('files/' + last_post.profile_type):
            if last_post.filename in f:
                filename = 'files/' + last_post.profile_type + '/' + f
                ext = f.split('.')[1]

                if ext == 'jpg':
                    image = open(filename, 'rb')
                    bot.send_photo(user_id, image, timeout=10, reply_markup=keyboards.main_menu_keyboard)
                    image.close()

                elif ext == 'mp4':
                    video = open(filename, 'rb')
                    bot.send_video(user_id, video, timeout=60, reply_markup=keyboards.main_menu_keyboard)
                    video.close()

                os.remove(filename)

        db_manager.delete_post(last_post.post_id);

        bot.send_message(user_id,
                        post_text,
                        reply_markup=keyboards.main_menu_keyboard,
                        parse_mode='HTML')