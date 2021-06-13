import telebot

# main menu
main_menu_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
main_menu_keyboard_fetch_posts_button = telebot.types.KeyboardButton("Fetch posts")
main_menu_keyboard_next_post_button = telebot.types.KeyboardButton("Next post")
main_menu_keyboard_add_profile_button = telebot.types.KeyboardButton("Add profile")
main_menu_keyboard_add_criteria_button = telebot.types.KeyboardButton("Add criteria")
main_menu_keyboard.add(main_menu_keyboard_add_profile_button, main_menu_keyboard_add_criteria_button)
main_menu_keyboard.add(main_menu_keyboard_fetch_posts_button, main_menu_keyboard_next_post_button)


# select profile
select_profile_type_inline_keyboard = telebot.types.InlineKeyboardMarkup()
select_profile_inline_button_instagram = telebot.types.InlineKeyboardButton(text='Instagram',
                                                                        callback_data='select_profile_instagram')
select_profile_inline_button_facebook = telebot.types.InlineKeyboardButton(text='Facebook',
                                                                        callback_data='select_profile_facebook')
select_profile_inline_button_youtube = telebot.types.InlineKeyboardButton(text='YouTube',
                                                                        callback_data='select_profile_youtube')
select_profile_type_inline_keyboard.add(select_profile_inline_button_instagram)
select_profile_type_inline_keyboard.add(select_profile_inline_button_facebook)
select_profile_type_inline_keyboard.add(select_profile_inline_button_youtube)


# select criteria
select_criteria_type_inline_keyboard = telebot.types.InlineKeyboardMarkup()
select_criteria_inline_button_likesviews = telebot.types.InlineKeyboardButton(text='Likes/views',
                                                                        callback_data='select_criteria_likesviews')
select_criteria_inline_button_hasvideo = telebot.types.InlineKeyboardButton(text='Includes video',
                                                                        callback_data='select_criteria_hasvideo')
select_criteria_type_inline_keyboard.add(select_criteria_inline_button_likesviews)
select_criteria_type_inline_keyboard.add(select_criteria_inline_button_hasvideo)


# cancel keyboard
cancel_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
cancel_keyboard.add('Охрана')
