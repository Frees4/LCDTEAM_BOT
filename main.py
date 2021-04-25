import telebot
import flask
from telebot import types
import db_funcs
import google_funcs
import datetime
import calendar
import re
from make_keyboards import *
from bot_funcs import *
from concurrency import coroutine, sleep, run


reader = open('token.txt', 'r')
TOKEN = reader.read()
APP_NAME = 'lcdnautraineebot'
bot = telebot.TeleBot(TOKEN)


internship_jobs = ['Стажер-разработчик Java', 'Стажер-тестировщик',
                    'Стажер-аналитик', 'Стажер технический писатель']
internship_cities = ['Екатеринбург', 'Краснодар', 'Санкт-Петербург', 'Челябинск', 'Тверь', ]
internship_timespend = ['40 часов', '>30 часов', '<30 часов']
internship_workafterintern = ['нет, только на период стажировки',
                                'да, полный рабочий день',
                                'да, неполный рабочий день']
edu_types = ['высшее', 'незаконченное высшее', 'среднее профессиональное', 'другое']
sources_info_naumen = ['сайт компании', 'реклама в интернете', 'на сайте hh.ru',
                        'обр. программа компании', 'социальные сети',
                        'от знакомых', 'стенды в вузе',
                        'другое']
city_vacancies = ['ekb_vacancies', 'krd_vacancies', 'spb_vacancies',
                    'chlb_vacancies', 'tvr_vacancies']
city_tags = ['ekb', 'krasnodar', 'spb', 'chlb', 'tvr']

@coroutine
def ping(bot, timeout):
    while True:
        yield from sleep(timeout)
        print(datetime.datetime.now())
        user_ids = db_funcs.get_users_notfilled()
        for user_id in user_ids:
            bot.send_message(chat_id=user_id,
                                text="Заполните анкету до конца и убедитесь, что вы выполнили тестовое задание",
                                reply_markup=None)
        changes = False
        i = 0
        old_vacancies = []
        new_vacancies = []
        for i in range(len(city_tags)):
            old_vacancies = db_funcs.get_parameters('vacancies.db',
                                                city_vacancies[i],'name_internship')
            new_vacancies = get_vacancies_list(city_tags[i])
            if (old_vacancies != new_vacancies):
                changes = True
                db_funcs.clear_table_vacancies(city_vacancies[i])
                db_funcs.change_vacancies(city_vacancies[i], new_vacancies)
        if (changes is True):
            user_ids = db_funcs.get_parameters('users.db', 'subscribers', 'tg_id')
            for user_id in user_ids:
                bot.send_message(chat_id=user_id,
                                text="Список стажировок изменился!",
                                reply_markup=make_welcome_actions_keyboard())


@bot.message_handler(commands=['help'])
def answer(message):
    bot.send_message(chat_id=message.chat.id,
                    text="test",
                    reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if (db_funcs.check_user_in_db('users.db', 'users', message.chat.id) is False):
        db_funcs.add_user_to_db('users.db', 'users', message.chat.id)
        db_funcs.end_filling('users.db', 'users', message.chat.id)
    if (db_funcs.check_filling('users.db', 'users', message.chat.id) == 0):
        if ( message.text.lower() == 'работа с анкетой' ):
            keyboard = make_form_actions_keyboard(message.chat.id)
            bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)
        elif ( message.text.lower() == 'сформировать новую анкету' ):
            create_new_form(message.chat.id)
        elif ( message.text.lower() == 'просмотр вакансий' ):
            show_vacancy_cities(bot, message.chat.id)
        elif ( message.text.lower() == 'правила приема на стажировку'):
            file = open('rules.txt', 'r', encoding='utf-8')
            string = ''
            for line in file.readlines():
                string += (line)
            file.close()
            bot.send_message(chat_id=message.chat.id,
                            text=string,
                            reply_markup=make_welcome_actions_keyboard())
        elif ( message.text.lower() == 'подписаться на рассылку' ):
            db_funcs.add_user_to_subscribers(message.chat.id)
            bot.send_message(chat_id=message.chat.id,
                            text="Вы подписались на рассылку уведомлений о новых стажировках.",
                            reply_markup=make_welcome_actions_keyboard())
        elif ( message.text.lower() == 'отписаться от рассылки' ):
            db_funcs.delete_user_from_db('users.db', 'subscribers', message.chat.id)
            bot.send_message(chat_id=message.chat.id,
                            text="Вы отписались от рассылки уведомлений о новых стажировках.",
                            reply_markup=make_welcome_actions_keyboard())
        elif ( message.text.lower() == 'не подписываться' or message.text.lower() == 'не отписываться'):
            bot.send_message(chat_id=message.chat.id,
                            text="Выберите действие",
                            reply_markup=make_welcome_actions_keyboard())
    else:
        if (message.text.lower() == 'отправить форму'):
            send_form(bot, message.chat.id)
        elif (message.text.lower() == 'просмотреть анкету'):
            show_form(bot, message.chat.id)
        elif (message.text.lower() == 'отменить заполнение'):
            try:
                db_funcs.delete_user_from_db('users.db', 'users', message.chat.id)
            except:
                pass
            bot.send_message(chat_id=message.chat.id,
                            text="Заполнение формы отменено",
                            reply_markup=make_welcome_actions_keyboard())
        else:
            # получаем прогресс заполнения формы пользователем
            progress = db_funcs.get_progress('users.db', 'users', message.chat.id)
            if (progress == 2):
                if (re.fullmatch(pattern="^[A-Za-zА-Яа-я]+$",
                                string=message.text)):
                    db_funcs.update_cell(db_name='users.db',
                                        tablename='users',
                                        tg_id=message.chat.id,
                                        progress=3,
                                        cell_name="surname_intern",
                                        cell_value=message.text)
                    bot.send_message(chat_id=message.chat.id,
                                    text="Введите имя",
                                    reply_markup=make_formcancel_keyboard())
                else:
                    bot.send_message(chat_id=message.chat.id,
                                    text="Повторите ввод",
                                    reply_markup=make_formcancel_keyboard())
            elif (progress == 3):
                # при вводе имени
                if (re.fullmatch(pattern="^[A-Za-zА-Яа-я]+$",
                                string=message.text)):
                    db_funcs.update_cell(db_name='users.db',
                                        tablename='users',
                                        tg_id=message.chat.id,
                                        progress=4,
                                        cell_name="name_intern",
                                        cell_value=message.text)
                    bot.send_message(chat_id=message.chat.id,
                                    text="Введите отчество",
                                    reply_markup=make_formcancel_keyboard())
                else:
                    bot.send_message(chat_id=message.chat.id,
                                    text="Повторите ввод",
                                    reply_markup=make_formcancel_keyboard())
            elif (progress == 4):
                # при вводе отчества
                if (re.fullmatch(pattern="^[A-Za-zА-Яа-я]+$",
                                string=message.text)):
                    db_funcs.update_cell(db_name='users.db',
                                        tablename='users',
                                        tg_id=message.chat.id,
                                        progress=5,
                                        cell_name="patronymics_intern",
                                        cell_value=message.text)
                    bot.send_message(chat_id=message.chat.id,
                                    text="Введите дату рождения в формате дд.мм.гггг",
                                    reply_markup=make_formcancel_keyboard())
                else:
                    bot.send_message(chat_id=message.chat.id,
                                    text="Повторите ввод",
                                    reply_markup=make_formcancel_keyboard())
            elif (progress == 5):
                if (re.fullmatch(pattern="^(0?[1-9]|[12]\d|30|31)[.](0?[1-9]|1[0-2])[.](\d{4})$",
                        string=message.text) is not None and datetime.datetime.now().year > int(message.text[6:10])):
                    db_funcs.update_cell(db_name='users.db',
                                        tablename='users',
                                        tg_id=message.chat.id,
                                        progress=6,
                                        cell_name="date_of_birth",
                                        cell_value=message.text)
                    bot.send_message(chat_id=message.chat.id,
                                    text="Введите город проживания",
                                    reply_markup=make_formcancel_keyboard())
                else:
                    if (datetime.datetime.now().year <= int(message.text[6:10])):
                        bot.send_message(chat_id=message.chat.id,
                                        text="Введите корректную дату",
                                        reply_markup=make_formcancel_keyboard())
                    else:
                        bot.send_message(chat_id=message.chat.id,
                                        text="Неверный формат, повторите ввод в формате дд.мм.гггг",
                                        reply_markup=make_formcancel_keyboard())
            elif (progress == 6):
                if (re.fullmatch(pattern="^[A-Za-zА-Яа-я]+$",
                                string=message.text)):
                    db_funcs.update_cell(db_name='users.db',
                                        tablename='users',
                                        tg_id=message.chat.id,
                                        progress=7,
                                        cell_name="city_living",
                                        cell_value=message.text)
                    bot.send_message(chat_id=message.chat.id,
                                    text="Введите адрес электронной почты",
                                    reply_markup=make_formcancel_keyboard())
                else:
                    bot.send_message(chat_id=message.chat.id,
                                    text="Повторите ввод",
                                    reply_markup=make_formcancel_keyboard())
            elif (progress == 7):
                if (re.fullmatch(pattern="""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""",
                                string=message.text)):
                    db_funcs.update_cell(db_name='users.db',
                                        tablename='users',
                                        tg_id=message.chat.id,
                                        progress=8,
                                        cell_name="email",
                                        cell_value=message.text)
                    bot.send_message(chat_id=message.chat.id,
                                    text="Введите номер телефона или поставьте прочерк -",
                                    reply_markup=make_formcancel_keyboard())
                else:
                    bot.send_message(chat_id=message.chat.id,
                                    text="Неверный формат, повторите ввод",
                                    reply_markup=make_formcancel_keyboard())
            elif (progress == 8):
                if (message.text == '-' or re.fullmatch(
                                            pattern="^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$",
                                            string=message.text)):
                    db_funcs.update_cell(db_name='users.db',
                                        tablename='users',
                                        tg_id=message.chat.id,
                                        progress=9,
                                        cell_name="telnumber",
                                        cell_value=message.text)
                    bot.send_message(chat_id=message.chat.id,
                                    text="Когда сможете приступить к стажировке? В формате дд.мм.гггг",
                                    reply_markup=make_formcancel_keyboard())
                else:
                    bot.send_message(chat_id=message.chat.id,
                                    text="Неверный формат, повторите ввод",
                                    reply_markup=make_formcancel_keyboard())
            elif (progress == 9):
                if (re.fullmatch(pattern="^(0?[1-9]|[12]\d|30|31)[.](0?[1-9]|1[0-2])[.](\d{4})$",
                        string=message.text) is not None and datetime.datetime.strptime(message.text, "%d.%m.%Y") > datetime.datetime.now()):
                    db_funcs.update_cell(db_name='users.db',
                                        tablename='users',
                                        tg_id=message.chat.id,
                                        progress=10,
                                        cell_name="date_of_start",
                                        cell_value=message.text)
                    bot.send_message(chat_id=message.chat.id,
                                    text="Сколько времени в неделю ты готов уделять стажировке?",
                                    reply_markup=make_choose_keyboard(internship_timespend))
                else:
                    if (re.fullmatch(pattern="^(0?[1-9]|[12]\d|30|31)[.](0?[1-9]|1[0-2])[.](\d{4})$",
                        string=message.text) is not None and datetime.datetime.strptime(message.text, "%d.%m.%Y") <= datetime.datetime.now()):
                        bot.send_message(chat_id=message.chat.id,
                                        text="Введите корректную дату",
                                        reply_markup=make_formcancel_keyboard())
                    else:
                        bot.send_message(chat_id=message.chat.id,
                                        text="Неверный формат, повторите ввод в формате дд.мм.гггг",
                                        reply_markup=make_formcancel_keyboard())
            elif (progress == 13 or progress == 20):
                if (progress == 13):
                    cell_tempname = "edu_name"
                else:
                    cell_tempname = "edu2_name"
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=progress+1,
                                    cell_name=cell_tempname,
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Введите год поступления",
                                reply_markup=None)
            elif (progress == 14 or progress == 21):
                if (progress == 14):
                    cell_tempname = "edu_year_start"
                else:
                    cell_tempname = "edu2_year_start"
                if (re.fullmatch(pattern="^(19|20)\d{2}$",
                        string=message.text) is not None and
                        datetime.datetime.now().year >= int(message.text)):
                    db_funcs.update_cell(db_name='users.db',
                                        tablename='users',
                                        tg_id=message.chat.id,
                                        progress=progress+1,
                                        cell_name=cell_tempname,
                                        cell_value=message.text)
                    bot.send_message(chat_id=message.chat.id,
                                    text="Введите год окончания",
                                    reply_markup=None)
                else:
                    if (re.fullmatch(pattern="^(19|20)\d{2}$", string=message.text) is not None
                            and datetime.datetime.now().year <= int(message.text)):
                        bot.send_message(chat_id=message.chat.id,
                                        text="Введите корректную дату",
                                        reply_markup=make_formcancel_keyboard())
                    else:
                        bot.send_message(chat_id=message.chat.id,
                                        text="Неверный формат, повторите ввод",
                                        reply_markup=make_formcancel_keyboard())
            elif (progress == 15 or progress == 22):
                if (progress == 15):
                    cell_tempname = "edu_year_end"
                else:
                    cell_tempname = "edu2_year_end"
                if (re.fullmatch(pattern="^(19|20)\d{2}$",
                        string=message.text) is not None):
                    db_funcs.update_cell(db_name='users.db',
                                        tablename='users',
                                        tg_id=message.chat.id,
                                        progress=progress + 1,
                                        cell_name=cell_tempname,
                                        cell_value=message.text)
                    bot.send_message(chat_id=message.chat.id,
                                    text="Введите название факультета и специальности",
                                    reply_markup=None)
                else:
                    bot.send_message(chat_id=message.chat.id,
                                    text="Неверный формат, повторите ввод",
                                    reply_markup=make_formcancel_keyboard())
            elif (progress == 16 or progress == 23):
                if (progress == 16):
                    cell_tempname = "edu_faculty"
                else:
                    cell_tempname = "edu2_faculty"
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=progress+1,
                                    cell_name=cell_tempname,
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Введите средний балл",
                                reply_markup=None)
            elif (progress == 17 or progress == 24):
                if (progress == 17):
                    cell_tempname = "edu_score"
                else:
                    cell_tempname = "edu2_score"
                if (re.fullmatch(pattern="^\d{1}$",
                                string=message.text) and int(message.text) <= 5):
                    db_funcs.update_cell(db_name='users.db',
                                        tablename='users',
                                        tg_id=message.chat.id,
                                        progress=progress+1,
                                        cell_name=cell_tempname,
                                        cell_value=message.text)
                    if (progress == 17):
                        bot.send_message(chat_id=message.chat.id,
                                        text="Есть ли у вас второе образование?",
                                        reply_markup=make_choose_keyboard(['Да', 'Нет']))
                    else:
                        bot.send_message(chat_id=message.chat.id,
                            text="""Есть ли у вас дополнительное образование? Напишите о нем или оставьте прочерк -""",
                            reply_markup=None)
                else:
                    bot.send_message(chat_id=message.chat.id,
                                    text="Неверный формат, введите одно число не больше 5",
                                    reply_markup=make_formcancel_keyboard())
            elif (progress == 25):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=26,
                                    cell_name="additive_edu",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Есть ли у вас опыт работы?",
                                reply_markup=make_choose_keyboard(['Да', 'Нет']))
            elif (progress == 27 or progress == 32 or progress == 37 or progress == 42):
                if (progress == 27):
                    cell_tempname = "time1"
                elif (progress == 32):
                    cell_tempname = "time2"
                elif (progress == 37):
                    cell_tempname = "time3"
                elif (progress == 42):
                    cell_tempname = "time4"
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=progress+1,
                                    cell_name=cell_tempname,
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Введите место работы",
                                reply_markup=None)
            elif (progress == 28 or progress == 33 or progress == 38 or progress == 43):
                if (progress == 28):
                    cell_tempname = "place1"
                elif (progress == 33):
                    cell_tempname = "place2"
                elif (progress == 38):
                    cell_tempname = "place3"
                elif (progress == 43):
                    cell_tempname = "place4"
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=progress+1,
                                    cell_name=cell_tempname,
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Введите должность",
                                reply_markup=None)
            elif (progress == 29 or progress == 34 or progress == 39 or progress == 44):
                if (progress == 29):
                    cell_tempname = "rank1"
                elif (progress == 34):
                    cell_tempname = "rank2"
                elif (progress == 39):
                    cell_tempname = "rank3"
                elif (progress == 44):
                    cell_tempname = "rank4"
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=progress+1,
                                    cell_name=cell_tempname,
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Опишите ваши обязанности",
                                reply_markup=None)
            elif (progress == 30 or progress == 35 or progress == 40 or progress == 45):
                if (progress == 30):
                    cell_tempname = "duty1"
                elif (progress == 35):
                    cell_tempname = "duty2"
                elif (progress == 40):
                    cell_tempname = "duty3"
                elif (progress == 45):
                    cell_tempname = "duty4"
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=progress+1,
                                    cell_name=cell_tempname,
                                    cell_value=message.text)
                if (progress != 45):
                    bot.send_message(chat_id=message.chat.id,
                                    text="Добавить опыт работы",
                                    reply_markup=make_choose_keyboard(['Да', 'Нет']))
                else:
                    bot.send_message(chat_id=message.chat.id,
                                    text="В каких проектах вы принимали участие?",
                                    reply_markup=None)
            elif (progress == 46):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=47,
                                    cell_name="projects",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="""Участвовали ли вы в образовательных программах от Naumen? Если да, то расскажите об этом подробнее или поставьте прочерк -""",
                                reply_markup=None)
            elif (progress == 47):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=48,
                                    cell_name="naumen_eduprogs",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Какие свои навыки вы считаете ключевыми?",
                                reply_markup=None)
            elif (progress == 48):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=49,
                                    cell_name="key_skills",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Какие у вас профессиональные интересы?",
                                reply_markup=None)
            elif (progress == 49):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=50,
                                    cell_name="prof_interests",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Какую профессиональную книгу вы прочитали последней?",
                                reply_markup=None)
            elif (progress == 50):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=51,
                                    cell_name="last_read_book",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Как вы проводите свободное время? Какие у вас увлечения?",
                                reply_markup=None)
            elif (progress == 51):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=52,
                                    cell_name="hobbies",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Что даст тебе прохождение практики в нашей компании?",
                                reply_markup=None)
            elif (progress == 52):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=53,
                                    cell_name="expectations",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Какую должность ты хочешь занять через 3-5 лет?",
                                reply_markup=None)
            elif (progress == 53):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=54,
                                    cell_name="future_rank",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Как ты узнал о компании Naumen?",
                                reply_markup=make_choose_keyboard(sources_info_naumen))
            elif (progress == 55):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=56,
                                    cell_name="source_info_naumen",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                            text="Как ты узнал о стажировке в Naumen?",
                            reply_markup=make_choose_keyboard(sources_info_naumen))
            elif (progress == 57):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=59,
                                    cell_name="source_info_internship",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="""Кто может дать вам рекомендации?
                                        (ФИО, должность, контактный телефон)""",
                                reply_markup=None)
            elif (progress == 58):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=59,
                                    cell_name="recommendations_authors",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Приложите ссылку на резюме на hh.ru, если оно есть или оставьте прочерк -",
                                reply_markup=None)
            elif (progress == 59):
                if (re.fullmatch(pattern="^(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,})$",
                                string=message.text) or message.text == '-'):
                    db_funcs.update_cell(db_name='users.db',
                                        tablename='users',
                                        tg_id=message.chat.id,
                                        progress=60,
                                        cell_name="summary_hhlink",
                                        cell_value=message.text)
                    bot.send_message(chat_id=message.chat.id,
                                    text="Приложите ссылку на папку с тестовым заданием в облаке",
                                    reply_markup=None)
                else:
                    bot.send_message(chat_id=message.chat.id,
                                    text="Неправильный формат, повторите ввод",
                                    reply_markup=None)
            elif (progress == 60):
                if (re.fullmatch(pattern="^(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,})$",
                                string=message.text)):
                    db_funcs.update_cell(db_name='users.db',
                                        tablename='users',
                                        tg_id=message.chat.id,
                                        progress=100,
                                        cell_name="task_link",
                                        cell_value=message.text)
                    bot.send_message(chat_id=message.chat.id,
                                    text="Вы заполнили все поля анкеты. Выберите действие:",
                                    reply_markup=make_actions_endfill_keyboard())
                else:
                    bot.send_message(chat_id=message.chat.id,
                                    text="Неправильный формат. Повторите ввод",
                                    reply_markup=None)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'new_agree':
        db_funcs.delete_user_from_db('users.db', 'users', tg_id)
        db_funcs.start_filling('users.db', 'users', tg_id)
        bot.send_message(chat_id=call.message.chat.id,
                        text='Начинаем процесс регистрации',
                        reply_markup=make_formcancel_keyboard())
        
        available_cities = []
        for i in range(len(internship_cities)):
            if (len(get_vacancies_list(city_tags[i])) > 0):
                available_cities.append(internship_cities[i])
        bot.send_message(chat_id=call.message.chat.id,
                        text='Выберите город прохождения стажировки',
                        reply_markup=make_choose_keyboard(available_cities))
    elif call.data == 'new_disagree':
        bot.send_message(chat_id=call.message.chat.id,
                        text="Создание новой анкеты было отменено",
                        reply_markup=make_welcome_actions_keyboard())
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                    message_id=call.message.id,
                                    reply_markup=None)
    elif (call.data in internship_cities):
        db_funcs.update_cell(db_name='users.db',
                            tablename='users',
                            tg_id=call.message.chat.id,
                            progress=1,
                            cell_name="city_internship",
                            cell_value=call.data)
        bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.id,
                            text="Выбран город: %s" % call.data,
                            reply_markup=None)
        tag = 'ekb'
        for i in range(len(internship_cities)):
            if (call.data == internship_cities[i]):
                tag = city_tags[i]
                break
        vacancies = get_vacancies_list(tag)
        bot.send_message(chat_id=call.message.chat.id,
                        text="Выберите специальность",
                        reply_markup=make_choose_keyboard(vacancies))
    elif (call.data in city_vacancies):
        if (call.data == 'ekb_vacancies'):
            city_name = 'Екатеринбург'
            show_vacancies(bot, call.message.chat.id, 'ekb')
        elif (call.data == 'krd_vacancies'):
            city_name = 'Краснодар'
            show_vacancies(bot, call.message.chat.id, 'krasnodar')
        elif (call.data == 'spb_vacancies'):
            city_name = 'Санкт-Петербург'
            show_vacancies(bot, call.message.chat.id, 'spb')
        elif (call.data == 'chlb_vacancies'):
            city_name = 'Челябинск'
            show_vacancies(bot, call.message.chat.id, 'chlb')
        elif (call.data == 'tvr_vacancies'):
            city_name = 'Тверь'
            show_vacancies(bot, call.message.chat.id, 'tvr')
        bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.id,
                            text="Выбран город "+city_name,
                            reply_markup=None)
    elif (call.data in internship_jobs
                and db_funcs.check_filling('users.db', 'users', call.message.chat.id) == 0):
        if (call.data == google_funcs.list_name_java):
            filename = "javadev.txt"
        elif (call.data == google_funcs.list_name_tester):
            filename = "tester.txt"
        elif (call.data == google_funcs.list_name_analytics):
            filename = "analytic.txt"
        elif (call.data == google_funcs.list_name_techwriter):
            filename = "techwriter.txt"
        file = open(filename, 'r', encoding='utf-8')
        string = ''
        for line in file.readlines():
            string += (line+)
        file.close()
        bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.id,
                            text="Выбрана специальность "+call.data.lower(),
                            reply_markup=None)
        bot.send_message(chat_id=call.message.chat.id,
                        text=string,
                        reply_markup=make_welcome_actions_keyboard())

    elif (call.data in internship_jobs 
                and db_funcs.check_filling('users.db', 'users', call.message.chat.id) == 1):
        db_funcs.update_cell(db_name='users.db',
                            tablename='users',
                            tg_id=call.message.chat.id,
                            progress=2,
                            cell_name="name_internship",
                            cell_value=call.data)
        bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.id,
                            text="Выбрана специальность стажировки: %s\nВ файле ниже тестовое задание." % call.data.lower(),
                            reply_markup=None)
        if (call.data == google_funcs.list_name_java):
            filename = 'javatask.pdf'
        elif (call.data == google_funcs.list_name_tester):
            filename = 'testertask.pdf'
        elif (call.data == google_funcs.list_name_analytics):
            filename = 'analytictask.pdf'
        elif (call.data == google_funcs.list_name_techwriter):
            filename = 'techwriter.pdf'
        bot.send_document(chat_id=call.message.chat.id,
                        data=open(filename, 'rb'))
        bot.send_message(chat_id=call.message.chat.id,
                        text="Введите фамилию",
                        reply_markup=make_formcancel_keyboard())
    elif (call.data in internship_timespend):
        db_funcs.update_cell(db_name='users.db',
                            tablename='users',
                            tg_id=call.message.chat.id,
                            progress=11,
                            cell_name="time_spend",
                            cell_value=call.data)
        bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.id,
                            text="Выбрано количество времени, уделяемого стажировке: %s" % call.data,
                            reply_markup=None)
        bot.send_message(chat_id=call.message.chat.id,
                        text="Сможете продолжать работу после окончания стажировки?",
                        reply_markup=make_choose_keyboard(internship_workafterintern))
    elif (call.data in internship_workafterintern):
        db_funcs.update_cell(db_name='users.db',
                            tablename='users',
                            tg_id=call.message.chat.id,
                            progress=12,
                            cell_name="work_after_internship",
                            cell_value=call.data)
        bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.id,
                            text="Возможность продолжить работу после окончания стажировки: %s" % call.data,
                            reply_markup=None)
        bot.send_message(chat_id=call.message.chat.id,
                        text="Выберите тип полученного образования:",
                        reply_markup=make_choose_keyboard(edu_types))
    elif (call.data in edu_types and db_funcs.get_progress('users.db', 'users', call.message.chat.id) < 38):
        if (db_funcs.get_progress('users.db', 'users', call.message.chat.id) <= 17):
            temp_progress = 13
            temp_cellname = "`edu_type`"
        else:
            temp_progress = 20
            temp_cellname = "`edu2_type`"
        db_funcs.update_cell(db_name='users.db',
                            tablename='users',
                            tg_id=call.message.chat.id,
                            progress=temp_progress,
                            cell_name=temp_cellname,
                            cell_value=call.data)
        bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.id,
                            text="Тип полученного образования: %s" % call.data,
                            reply_markup=None)
        bot.send_message(chat_id=call.message.chat.id,
                        text="Введите наименование учебного заведения:",
                        reply_markup=None)
    elif (db_funcs.get_progress('users.db', 'users', call.message.chat.id) == 18):
        if (call.data.lower() == 'да'):
            db_funcs.update_cell(db_name='users.db',
                                tablename='users',
                                tg_id=call.message.chat.id,
                                progress=19,
                                cell_name="`edu2_exist`",
                                cell_value=1)
            bot.send_message(chat_id=call.message.chat.id,
                        text="Выберите тип полученного образования:",
                        reply_markup=make_choose_keyboard(edu_types))
        else:
            db_funcs.update_cell(db_name='users.db',
                                tablename='users',
                                tg_id=call.message.chat.id,
                                progress=25,
                                cell_name="`edu2_exist`",
                                cell_value=0)
            bot.send_message(chat_id=call.message.chat.id,
                            text="""Есть ли у вас дополнительное образование? Напишите о нем или оставьте прочерк -""",
                            reply_markup=None)
        bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.id,
                                text="Имеется второе образование: %s" % call.data,
                                reply_markup=None)
    elif (db_funcs.get_progress('users.db', 'users', call.message.chat.id) == 26 or
            db_funcs.get_progress('users.db', 'users', call.message.chat.id) == 31 or
            db_funcs.get_progress('users.db', 'users', call.message.chat.id) == 36 or
            db_funcs.get_progress('users.db', 'users', call.message.chat.id) == 41):
        progress = db_funcs.get_progress('users.db', 'users', call.message.chat.id)
        bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.id,
                                text="Есть ли у вас опыт работы: %s" % call.data,
                                reply_markup=None)
        if call.data.lower() == 'да':
            if progress == 26:
                cell_tempname = "jobexp1_exist"
            elif progress == 31:
                cell_tempname = "jobexp2_exist"
            elif progress == 36:
                cell_tempname = "jobexp3_exist"
            elif progress == 41:
                cell_tempname = "jobexp4_exist"
            db_funcs.update_cell(db_name='users.db',
                                tablename='users',
                                tg_id=call.message.chat.id,
                                progress=progress+1,
                                cell_name=cell_tempname,
                                cell_value=1)
            bot.send_message(chat_id=call.message.chat.id,
                            text="Введите период работы (с ... до ...)",
                            reply_markup=None)
        else:
            db_funcs.update_cell(db_name='users.db',
                                tablename='users',
                                tg_id=call.message.chat.id,
                                progress=46,
                                cell_name="jobexp1_exist",
                                cell_value=0)
            bot.send_message(chat_id=call.message.chat.id,
                            text="В каких проектах вы принимали участие?",
                            reply_markup=None)
    elif (call.data in sources_info_naumen and
            db_funcs.get_progress('users.db', 'users', call.message.chat.id) == 54):
        bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.id,
                            text="Источник информации о компании: %s" % call.data,
                            reply_markup=None)
        if (call.data == 'другое'):
            bot.send_message(chat_id=call.message.chat.id,
                            text="Укажите источник",
                            reply_markup=None)
            db_funcs.update_progress(db_name='users.db', tablename='users',
                                    tg_id=call.message.chat.id, progress=55)
        else:
            db_funcs.update_cell(db_name='users.db',
                                tablename='users',
                                tg_id=call.message.chat.id,
                                progress=56,
                                cell_name="source_info_naumen",
                                cell_value=call.data)
            bot.send_message(chat_id=call.message.chat.id,
                            text="Как вы узнали о стажировке в Naumen?",
                            reply_markup=make_choose_keyboard(sources_info_naumen))
    elif (call.data in sources_info_naumen and
            db_funcs.get_progress('users.db', 'users', call.message.chat.id) == 56):
        bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.id,
                            text="Источник информации о стажировке: %s" % call.data,
                            reply_markup=None)
        if (call.data == 'другое'):
            bot.send_message(chat_id=call.message.chat.id,
                            text="Укажите источник",
                            reply_markup=None)
            db_funcs.update_progress(db_name='users.db', tablename='users',
                                    tg_id=call.message.chat.id, progress=57)
        else:
            db_funcs.update_cell(db_name='users.db',
                                tablename='users',
                                tg_id=call.message.chat.id,
                                progress=58,
                                cell_name="source_info_internship",
                                cell_value=call.data)
            bot.send_message(chat_id=call.message.chat.id,
                            text="Кто может дать вам рекомендации? (ФИО, должность, контактный телефон)",
                            reply_markup=None)





def create_new_form(tg_id):
        db_funcs.delete_user_from_db('users.db', 'users', tg_id)
        db_funcs.add_user_to_db('users.db', 'users', tg_id)
        db_funcs.start_filling('users.db', 'users', tg_id)
        bot.send_message(chat_id=tg_id,
                        text='Начинаем процесс регистрации',
                        reply_markup=make_formcancel_keyboard())
        available_cities = []
        for i in range(len(internship_cities)):
            if (len(get_vacancies_list(city_tags[i])) > 0):
                available_cities.append(internship_cities[i])
        bot.send_message(chat_id=tg_id,
                        text='Выберите город прохождения стажировки',
                        reply_markup=make_choose_keyboard(available_cities))



ping(bot, 86400) # 24 часа = 60*60*24 = 86400 секунд
keyboard = types.ReplyKeyboardMarkup()
buttonWorkForms = types.KeyboardButton('Работа с анкетой')
buttonShowVacancies = types.KeyboardButton('Просмотр вакансий')
keyboard.row(buttonWorkForms, buttonShowVacancies)
bot.polling(none_stop=True)
# сразу забиваем клавиатуру действий
# это нужно, чтобы у нас не прекращалось все действо
while True:
    pass