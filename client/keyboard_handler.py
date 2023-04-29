from telebot import types

class KeyboardHandler:
    def make_actions_endfill_keyboard(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton("Отправить форму"))
        keyboard.add(types.KeyboardButton("Просмотреть анкету"))
        keyboard.add(types.KeyboardButton("Отменить заполнение"))
        return keyboard


    def make_choose_keyboard(self, items_list):
        keyboard = types.InlineKeyboardMarkup()
        for item in items_list:
            keyboard.add(types.InlineKeyboardButton(text=item,
                                                    callback_data=item))
        return keyboard


    def make_choose_timespend_keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='40 часов (полн. рабочий день)',
                                                    callback_data='40 часов'))
        keyboard.add(types.InlineKeyboardButton(text='>30 часов',
                                                    callback_data='>30 часов'))
        keyboard.add(types.InlineKeyboardButton(text='<30 часов',
                                                    callback_data='<30 часов'))
        return keyboard


    def make_choose_job_keyboard(self):
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


    def make_choose_city_keyboard(self):
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


    def make_form_actions_keyboard(self, tg_id):
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        keyboard.add(types.KeyboardButton('Сформировать новую анкету'))
        return keyboard

    def make_welcome_actions_keyboard(self):
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        keyboard.add(types.KeyboardButton('Работа с анкетой'))
        keyboard.add(types.KeyboardButton('Просмотр вакансий'))
        keyboard.add(types.KeyboardButton('Правила приема на стажировку'))
        return keyboard


    def make_formcancel_keyboard(self):
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        keyboard.add(types.KeyboardButton('Отменить заполнение'))
        return keyboard