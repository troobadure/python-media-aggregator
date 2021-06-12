import telebot

# main menu
main_menu_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
main_menu_keyboard_fetch_posts_button = telebot.types.KeyboardButton("fetch posts")
main_menu_keyboard_get_post_button = telebot.types.KeyboardButton("get post")
main_menu_keyboard_add_profile_button = telebot.types.KeyboardButton("add profile")
main_menu_keyboard_add_criteria_button = telebot.types.KeyboardButton("add criteria")
main_menu_keyboard.add(main_menu_keyboard_add_profile_button, main_menu_keyboard_add_criteria_button)
main_menu_keyboard.add(main_menu_keyboard_fetch_posts_button, main_menu_keyboard_get_post_button)


# add profile
add_profile_inline_keyboard = telebot.types.InlineKeyboardMarkup()
add_profile_inline_button_insta = telebot.types.InlineKeyboardButton(text='Instagram',
                                                                     callback_data='add_profile_instagram')
add_profile_inline_button_facebook = telebot.types.InlineKeyboardButton(text='Facebook',
                                                                        callback_data='add_profile_facebook')
add_profile_inline_button_youtube = telebot.types.InlineKeyboardButton(text='YouTube',
                                                                       callback_data='add_profile_youtube')
add_profile_inline_keyboard.add(add_profile_inline_button_insta)
add_profile_inline_keyboard.add(add_profile_inline_button_facebook)
add_profile_inline_keyboard.add(add_profile_inline_button_youtube)


# add criteria
add_criteria_inline_keyboard = telebot.types.InlineKeyboardMarkup()
add_criteria_inline_button_insta = telebot.types.InlineKeyboardButton(text='Instagram',
                                                                      callback_data='add_criteria_instagram')
add_criteria_inline_button_facebook = telebot.types.InlineKeyboardButton(text='Facebook',
                                                                         callback_data='add_criteria_facebook')
add_criteria_inline_button_youtube = telebot.types.InlineKeyboardButton(text='YouTube',
                                                                        callback_data='add_criteria_youtube')
add_criteria_inline_keyboard.add(add_criteria_inline_button_insta)
add_criteria_inline_keyboard.add(add_criteria_inline_button_facebook)
add_criteria_inline_keyboard.add(add_criteria_inline_button_youtube)


# cancel keyboard
cancel_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
cancel_keyboard.add('Охрана')
