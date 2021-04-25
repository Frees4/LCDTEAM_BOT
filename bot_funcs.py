import telebot
from telebot import types
import db_funcs
import google_funcs
import datetime
import calendar
import re
from make_keyboards import *
from symbol import classdef
import requests
from bs4 import BeautifulSoup


def get_forms(bot, tg_id):
    bot.send_message(chat_id=tg_id,
                    text="Заглушка",
                    reply_markup=None)

def get_vacancies_list(tag):
    url = 'https://www.naumen.ru/career/trainee/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    results = soup.find_all("span", class_="trainee-t-line-city f16")
    vacancies = []
    for result in results:
        if (str(result.find('a').get('href')).find(tag) > 0):
            vacancies.append(result.find('a').text)
    return vacancies

def show_vacancies(bot, tg_id, tag):
    vacancies = get_vacancies_list(tag)
    keyboard = types.InlineKeyboardMarkup()
    for vacancy in vacancies:
        keyboard.add(types.InlineKeyboardButton(text=vacancy,
                                                callback_data=vacancy))
    bot.send_message(chat_id=tg_id,
                    text='Список доступных вакансий:',
                    reply_markup=keyboard)
    if (db_funcs.check_user_in_db('users.db', 'subscribers', tg_id) == 0):
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

def show_vacancy_cities(bot, tg_id):
    ekb_vacancies = get_vacancies_list('ekb')
    krd_vacancies = get_vacancies_list('krasnodar')
    spb_vacancies = get_vacancies_list('spb')
    chlb_vacancies = get_vacancies_list('chlb')
    tvr_vacancies = get_vacancies_list('tvr')
    keyboard = types.InlineKeyboardMarkup()
    if (len(ekb_vacancies) > 0):
        keyboard.add(types.InlineKeyboardButton(text='Екатеринбург',
                                                callback_data='ekb_vacancies'))
    if (len(krd_vacancies) > 0):
        keyboard.add(types.InlineKeyboardButton(text='Краснодар',
                                                callback_data='krd_vacancies'))
    if (len(spb_vacancies) > 0):
        keyboard.add(types.InlineKeyboardButton(text='Краснодар',
                                                callback_data='spb_vacancies'))
    if (len(chlb_vacancies) > 0):
        keyboard.add(types.InlineKeyboardButton(text='Краснодар',
                                                callback_data='chlb_vacancies'))
    if (len(tvr_vacancies) > 0):
        keyboard.add(types.InlineKeyboardButton(text='Краснодар',
                                                callback_data='tvr_vacancies'))
    bot.send_message(chat_id=tg_id,
                    text="Список городов для стажировок",
                    reply_markup=keyboard)
    if (db_funcs.check_user_in_db('users.db', 'subscribers', tg_id) == 0):
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

def show_form(bot, tg_id):
    userdata = db_funcs.get_userdata('users.db', 'users', tg_id)
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
                    reply_markup=make_actions_endfill_keyboard())


def send_form(bot, tg_id):
    userdata = db_funcs.get_userdata('users.db', 'users', tg_id)
    city_internship = userdata[12]
    list_name = userdata[4]
    if (list_name == google_funcs.list_name_java):
        tablename = db_funcs.tableJava
    if (list_name == google_funcs.list_name_analytics):
        tablename = db_funcs.tableAnalytics
    if (list_name == google_funcs.list_name_tester):
        tablename = db_funcs.tableTester
    if (list_name == google_funcs.list_name_techwriter):
        tablename = db_funcs.tableTechWriter
    if city_internship == 'Екатеринбург':
        table_id = google_funcs.table_ekb_id
        db_name = db_funcs.db_EKB
    elif city_internship == 'Санкт-Петербург':
        table_id = google_funcs.table_spb_id
        db_name = db_funcs.db_SPB
    elif city_internship == 'Челябинск':
        table_id = google_funcs.table_chlb_id
        db_name = db_funcs.db_CHLB
    elif city_internship == 'Краснодар':
        table_id = google_funcs.table_krd_id
        db_name = db_funcs.db_KRD
    elif city_internship == 'Тверь':
        table_id = google_funcs.table_tvr_id
        db_name = db_funcs.db_TVR
    result = []
    result.append(db_funcs.get_new_id(db_name, tablename))
    result.append(userdata[1]) # TG_id
    result.append(userdata[5]) # surname
    result.append(userdata[6]) # name
    result.append(userdata[7]) # patronymics
    result.append(userdata[8]) # date of birth
    result.append(userdata[9]) # city living
    result.append(userdata[10]) # email
    result.append(userdata[11]) # telnum
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
    result.append(userdata[44]) # work period
    result.append(userdata[45]) # work place
    result.append(userdata[46]) # work rank
    result.append(userdata[47]) # work duty
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
    result.append(userdata[27]) # summary hh link
    result.append(userdata[28]) # test task link
    vals = tuple(result)
    
    db_funcs.add_forminfo_table(db_name, tablename, result[1], vals)
    google_funcs.add_new_trainee(table_id, list_name, result[1:len(result)], result[0])
    bot.send_message(chat_id=tg_id,
                    text="Форма отправлена. По всем вопросам обращайтесь: nautrainee@naumen.ru",
                    reply_markup=make_welcome_actions_keyboard())
    db_funcs.end_filling('users.db', 'users', tg_id)