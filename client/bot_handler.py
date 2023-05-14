import telebot
from telebot import types
from core.facade import Facade
from client.keyboard_handler import KeyboardHandler
#from symbol import classdef
import requests
from bs4 import BeautifulSoup
from config import *


class BotHandler():
    def __init__(self):
        self.facade = Facade()
        self.keyboard_handler = KeyboardHandler()
        
    def get_forms(self, bot, tg_id):
        bot.send_message(chat_id=tg_id,
                        text="Заглушка",
                        reply_markup=None)

    def get_vacancies_list(self, tag):
        url = 'https://www.naumen.ru/career/trainee/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        results = soup.find_all("span", class_="trainee-t-line-city f16")
        vacancies = []
        for result in results:
            if (str(result.find('a').get('href')).find(tag) > 0):
                vacancies.append(result.find('a').text)
        return vacancies

    def show_vacancies(self, bot, tg_id, tag):
        vacancies = self.get_vacancies_list(tag)
        keyboard = types.InlineKeyboardMarkup()
        for vacancy in vacancies:
            keyboard.add(types.InlineKeyboardButton(text=vacancy,
                                                    callback_data=vacancy))
        bot.send_message(chat_id=tg_id,
                        text='Список доступных вакансий:',
                        reply_markup=keyboard)
        if (self.facade.check_user_in_db('data/users.db', 'subscribers', tg_id) == 0):
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            keyboard.add(types.KeyboardButton(text="Подписаться на рассылку"))
            keyboard.add(types.KeyboardButton(text="Не подписываться"))
            bot.send_message(chat_id=tg_id,
                        text="Вы можете подписаться на уведомления о стажировках",
                        reply_markup=keyboard)
        else:
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            keyboard.add(types.KeyboardButton(text="Отписаться от рассылки"))
            keyboard.add(types.KeyboardButton(text="Не отписываться"))
            bot.send_message(chat_id=tg_id,
                        text="Вы можете отписаться от уведомлений о стажировках",
                        reply_markup=keyboard)

    def show_vacancy_cities(self, bot, tg_id):
        ekb_vacancies = self.get_vacancies_list('ekb')
        krd_vacancies = self.get_vacancies_list('krasnodar')
        spb_vacancies = self.get_vacancies_list('spb')
        chlb_vacancies = self.get_vacancies_list('chlb')
        tvr_vacancies = self.get_vacancies_list('tvr')
        keyboard = types.InlineKeyboardMarkup()
        if (len(ekb_vacancies) > 0):
            keyboard.add(types.InlineKeyboardButton(text='Екатеринбург',
                                                    callback_data='ekb_vacancies'))
        if (len(krd_vacancies) > 0):
            keyboard.add(types.InlineKeyboardButton(text='Краснодар',
                                                    callback_data='krd_vacancies'))
        if (len(spb_vacancies) > 0):
            keyboard.add(types.InlineKeyboardButton(text='Санкт-Петербург',
                                                    callback_data='spb_vacancies'))
        if (len(chlb_vacancies) > 0):
            keyboard.add(types.InlineKeyboardButton(text='Челябинск',
                                                    callback_data='chlb_vacancies'))
        if (len(tvr_vacancies) > 0):
            keyboard.add(types.InlineKeyboardButton(text='Тверь',
                                                    callback_data='tvr_vacancies'))
        bot.send_message(chat_id=tg_id,
                        text="Список городов для стажировок",
                        reply_markup=keyboard)
        if (self.facade.check_user_in_db('data/users.db', 'subscribers', tg_id) == 0):
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            keyboard.add(types.KeyboardButton(text="Подписаться на рассылку"))
            keyboard.add(types.KeyboardButton(text="Не подписываться"))
            bot.send_message(chat_id=tg_id,
                        text="Вы можете подписаться на уведомления о стажировках",
                        reply_markup=keyboard)
        else:
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            keyboard.add(types.KeyboardButton(text="Отписаться от рассылки"))
            keyboard.add(types.KeyboardButton(text="Не отписываться"))
            bot.send_message(chat_id=tg_id,
                        text="Вы можете отписаться от уведомлений о стажировках",
                        reply_markup=keyboard)

    def show_form(self, bot, tg_id):
        userdata = self.facade.get_userdata('data/users.db', 'users', tg_id)
        result = "Город стажировки: %s\n" % userdata[12]
        result += "Специальность: %s\n" % userdata[4]
        result += "Фамилия: %s\n" % userdata[5]
        result += "Имя: %s\n" % userdata[6]
        result += "Отчество: %s\n" % userdata[7]
        result += "Дата рождения: %s\n" % userdata[8]
        result += "Город проживания: %s\n" % userdata[9]
        result += "Email: %s\n" % userdata[10]
        result += "Телефон: %s\n" % userdata[11]
        result += "Когда готов начать стажировку: %s\n" % userdata[13]
        result += "Сколько времени в неделю уделяется стажировке: %s\n" % userdata[14]
        result += "Возможность продолжить работу после окончания стажировки: %s\n" % userdata[15]
        result += "Тип полученного образования: %s\n" % userdata[29]
        result += "Название вуза: %s\n" % userdata[30]
        result += "Год начала обучения: %s\n" % userdata[31]
        result += "Год окончания обучения: %s\n" % userdata[32]
        result += "Факультет и специальность: %s\n" % userdata[33]
        result += "Средний балл: %s\n" % userdata[34]
        if (userdata[35] == 1):
            result += "Тип второго образования: %s\n" % userdata[36]
            result += "Название вуза: %s\n" % userdata[37]
            result += "Год начала обучения: %s\n" % userdata[38]
            result += "Год окончания обучения: %s\n" % userdata[39]
            result += "Факультет и специальность: %s\n" % userdata[40]
            result += "Средний балл: %s\n" % userdata[41]
        else:
            result += "Второе образование: отсутствует\n"
        result += "Дополнительное образование: %s\n" % userdata[42]
        if (userdata[43] == 1):
            result += "Наличие опыта работы: %s\n" % userdata[43]
            result += "Период работы: %s\n" % userdata[44]
            result += "Место работы: %s\n" % userdata[45]
            result += "Должность: %s\n" % userdata[46]
            result += "Обязанности: %s\n" % userdata[47]
            if (userdata[48] == 1):
                result += "Период работы: %s\n" % userdata[49]
                result += "Место работы: %s\n" % userdata[50]
                result += "Должность: %s\n" % userdata[51]
                result += "Обязанности: %s\n" % userdata[52]
            if (userdata[53] == 1):
                result += "Период работы: %s\n" % userdata[54]
                result += "Место работы: %s\n" % userdata[55]
                result += "Должность: %s\n" % userdata[56]
                result += "Обязанности: %s\n" % userdata[57]
            if (userdata[58] == 1):
                result += "Период работы: %s\n" % userdata[59]
                result += "Место работы: %s\n" % userdata[60]
                result += "Должность: %s\n" % userdata[61]
                result += "Обязанности: %s\n" % userdata[62]
        else:
            result += "Наличие опыта работы: нет\n"
        result += "Участие в проектах: %s\n" % userdata[16]
        result += "Участие в программах Naumen: %s\n" % userdata[17]
        result += "Ключевые навыки: %s\n" % userdata[18]
        result += "Профессиональные интересы: %s\n" % userdata[19]
        result += "Последняя прочитанная проф. книга: %s\n" % userdata[20]
        result += "Хобби: %s\n" % userdata[21]
        result += "Ожидания от стажировки: %s\n" % userdata[22]
        result += "Желаемая должность через 3-5 лет: %s\n" % userdata[23]
        result += "Источник информации о компании: %s\n" % userdata[24]
        result += "Источник информации о стажировке: %s\n" % userdata[25]
        result += "Кто может дать рекомендации: %s\n" % userdata[26]
        result += "Ссылка на резюме на hh: %s\n" % userdata[27]
        result += "Ссылка на тестовое задание: %s\n" % userdata[28]
        bot.send_message(chat_id=tg_id,
                        text=result,
                        reply_markup=self.keyboard_handler.make_actions_endfill_keyboard())


    def send_form(self, bot, tg_id):
        userdata = self.facade.get_userdata('data/users.db', 'users', tg_id)
        city_internship = userdata[12]
        list_name = userdata[4]
        if (list_name == 'Стажер-разработчик Java'):
            tablename = 'internJava'
        if (list_name == 'Стажер-аналитик'):
            tablename = 'internAnalytics'
        if (list_name == 'Стажер-тестировщик'):
            tablename = 'internTester'
        if (list_name == 'Стажер технический писатель'):
            tablename = 'internTechwriter'
        table_id = table_user_id
        db_name = db_users
        result = []
        result.append(self.facade.get_new_id(db_name, tablename))
        result.append(userdata[1]) # TG_id
        result.append(userdata[5]) # surname
        result.append(userdata[6]) # name
        result.append(userdata[7]) # patronymics
        result.append(userdata[8]) # date of birth
        result.append(userdata[9]) # city living
        result.append(userdata[10]) # email
        result.append(userdata[11]) # telnum
        result.append(userdata[28]) # test task link
        result.append(userdata[27]) # summary hh link
        result.append(userdata[13]) # date start internship
        result.append(userdata[14]) # time spend
        result.append(userdata[15]) # can work after
        result.append(userdata[29]) # edu type
        result.append(userdata[30]) # edu name
        result.append(userdata[31]) # edu start
        result.append(userdata[32]) # edu end
        result.append(userdata[33]) # edu faculty
        result.append(userdata[34]) # edu score
        result.append(userdata[36]) # edu2 type
        result.append(userdata[37]) # edu2 name
        result.append(userdata[38]) # edu2 start
        result.append(userdata[39]) # edu2 end
        result.append(userdata[40]) # edu2 faculty
        result.append(userdata[41]) # edu2 score
        result.append(userdata[42]) # edu additive
        result.append(userdata[43]) # job experience
        result.append(userdata[44]) # work period 1
        result.append(userdata[45]) # work place 1
        result.append(userdata[46]) # work rank 1
        result.append(userdata[47]) # work duty 1
        result.append(userdata[49]) # work period 2
        result.append(userdata[50]) # work place 2
        result.append(userdata[51]) # work rank 2
        result.append(userdata[52]) # work duty 2
        result.append(userdata[54]) # work period 3
        result.append(userdata[55]) # work place 3
        result.append(userdata[56]) # work rank 3
        result.append(userdata[57]) # work duty 3
        result.append(userdata[59]) # work period 4
        result.append(userdata[60]) # work place 4
        result.append(userdata[61]) # work rank 4
        result.append(userdata[62]) # work duty 4
        result.append(userdata[16]) # projects
        result.append(userdata[17]) # edu programms naumen
        result.append(userdata[18]) # key skills
        result.append(userdata[19]) # prof interests
        result.append(userdata[20]) # last read book
        result.append(userdata[21]) # hobbies
        result.append(userdata[22]) # expectations
        result.append(userdata[23]) # future rank
        result.append(userdata[24]) # source info company
        result.append(userdata[25]) # source info internship
        result.append(userdata[26]) # recomendations authors
        vals = tuple(result)
        
        self.facade.add_forminfo_table(db_name, tablename, result[1], vals)
        self.facade.add_new_trainee(table_id, list_name, result[1:len(result)], result[0])
        bot.send_message(chat_id=tg_id,
                        text="Форма отправлена. По всем вопросам обращайтесь: nautrainee@naumen.ru",
                        reply_markup=self.keyboard_handler.make_welcome_actions_keyboard())
        self.facade.end_filling('data/users.db', 'users', tg_id)
