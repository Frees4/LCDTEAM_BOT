from telebot import types
import db_funcs

def make_actions_endfill_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Отправить форму"))
    keyboard.add(types.KeyboardButton("Просмотреть анкету"))
    keyboard.add(types.KeyboardButton("Отменить заполнение"))
    return keyboard


def make_choose_keyboard(items_list):
    keyboard = types.InlineKeyboardMarkup()
    for item in items_list:
        keyboard.add(types.InlineKeyboardButton(text=item,
                                                callback_data=item))
    return keyboard


def make_choose_edutype_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    for item in edu_types:
        keyboard.add(types.InlineKeyboardButton(text=item.capitalize(),
                                                callback_data=item))
    return keyboard


def make_choose_workafterintern_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    for item in internship_workafterintern:
        keyboard.add(types.InlineKeyboardButton(text=item.capitalize(),
                                                callback_data=item))
    return keyboard


def make_choose_timespend_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='40 часов (полн. рабочий день)',
                                                callback_data='40 часов'))
    keyboard.add(types.InlineKeyboardButton(text='>30 часов',
                                                callback_data='>30 часов'))
    keyboard.add(types.InlineKeyboardButton(text='<30 часов',
                                                callback_data='<30 часов'))
    return keyboard


def make_choose_job_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Стажер-разработчик Java',
                                            callback_data='Стажер-разработчик Java'))
    keyboard.add(types.InlineKeyboardButton(text='Стажер-тестировщик',
                                            callback_data='Стажер-тестировщик'))
    keyboard.add(types.InlineKeyboardButton(text='Стажер-аналитик',
                                            callback_data='Стажер-аналитик'))
    keyboard.add(types.InlineKeyboardButton(text='Стажер технический писатель',
                                            callback_data='Стажер технический писатель'))
    return keyboard


def make_choose_city_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Екатеринбург',
                                                callback_data='Екатеринбург'))
    keyboard.add(types.InlineKeyboardButton(text='Краснодар',
                                                callback_data='Краснодар'))
    keyboard.add(types.InlineKeyboardButton(text='Санкт-Петербург',
                                                callback_data='Санкт-Петербург'))
    keyboard.add(types.InlineKeyboardButton(text='Челябинск',
                                                callback_data='Челябинск'))
    keyboard.add(types.InlineKeyboardButton(text='Тверь',
                                                callback_data='Тверь'))
    return keyboard


def make_form_actions_keyboard(tg_id):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Сформировать новую анкету'))
    #if (db_funcs.check_user_in_db('users.db', 'users', tg_id) is not False):
        #keyboard.add(types.KeyboardButton('Просмотреть свои анкеты'))
    keyboard.row()
    return keyboard


def make_welcome_actions_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Работа с анкетой'))
    keyboard.add(types.KeyboardButton('Просмотр вакансий'))
    keyboard.row()
    return keyboard


def make_formcancel_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Отменить заполнение'))
    return keyboard