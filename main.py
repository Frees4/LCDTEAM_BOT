import telebot
from telebot import types
import db_funcs
import google_funcs
import datetime
import calendar
import re
from make_keyboards import *


reader = open('token.txt', 'r')
TOKEN = reader.read()
bot = telebot.TeleBot(TOKEN)

internship_jobs = ['Стажер-разработчик Java', 'Стажер-тестировщик',
                    'Стажер-аналитик', 'Стажер технический писатель']
internship_cities = ['Екатеринбург', 'Москва', 'Санкт-Петербург', 'Челябинск', 'Тверь']
internship_timespend = ['40 часов', '>30 часов', '<30 часов']
internship_workafterintern = ['нет, только на период стажировки',
                                'да, полный рабочий день',
                                'да, неполный рабочий день']
edu_types = ['высшее', 'незаконченное высшее', 'среднее профессиональное', 'другое']
sources_info_naumen = ['сайт компании', 'реклама в интернете', 'на сайте hh.ru',
                        'обр. программа компании', 'социальные сети',
                        'от знакомых', 'стенды в вузе',
                        'другое']

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # создаем клавиатуру, make_actions_keyboard - моя функция, возвращает объект клавы
    # и находится ниже
    keyboard = make_welcome_actions_keyboard()
    # вызывается метод объекта бота с параметрами id чата, текстом сообщения и конфигом клавиатуры ответа
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)

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
        elif ( message.text.lower() == 'просмотреть свою анкету' and 
            db_funcs.check_user_in_db('users.db', 'users', message.chat.id) is True):
            pass
        elif ( message.text.lower() == 'просмотр вакансий' ):
            pass
    else:
        if (message.text.lower() == 'отправить форму'):
            pass
        elif (message.text.lower() == 'вернуться к шагу №'):
            pass
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
                if (re.fullmatch(pattern="(0?[1-9]|[12]\d|30|31)[^\w\d\r\n:](0?[1-9]|1[0-2])[^\w\d\r\n:](\d{4})",
                        string=message.text) is not None):
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
                if (re.fullmatch(pattern="(0?[1-9]|[12]\d|30|31)[^\w\d\r\n:](0?[1-9]|1[0-2])[^\w\d\r\n:](\d{4})",
                        string=message.text) is not None):
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
                    bot.send_message(chat_id=message.chat.id,
                                    text="Неверный формат, повторите ввод в формате дд.мм.гггг",
                                    reply_markup=make_formcancel_keyboard())
            elif (progress == 13 or progress == 19):
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
            elif (progress == 14 or progress == 20):
                if (progress == 14):
                    cell_tempname = "edu_year_start"
                else:
                    cell_tempname = "edu2_year_start"
                if (re.fullmatch(pattern="^(19|20)\d{2}$",
                        string=message.text) is not None):
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
                    bot.send_message(chat_id=message.chat.id,
                                    text="Неверный формат, повторите ввод",
                                    reply_markup=make_formcancel_keyboard())
            elif (progress == 15 or progress == 21):
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
            elif (progress == 16 or progress == 22):
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
            elif (progress == 17 or progress == 23):
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
                                    text="Неверный формат, введите одно число не больше 5",
                                    reply_markup=make_formcancel_keyboard())
            elif (progress == 24):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=25,
                                    cell_name="additive_edu",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Есть ли у вас опыт работы?",
                                reply_markup=make_choose_keyboard(['Да', 'Нет']))
            elif (progress == 26):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=27,
                                    cell_name="time",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Введите место работы",
                                reply_markup=None)
            elif (progress == 27):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=28,
                                    cell_name="place",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Введите должность",
                                reply_markup=None)
            elif (progress == 28):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=29,
                                    cell_name="duty",
                                    cell_value=message.text)
                bot.send_message(chat_id=call.message.chat.id,
                            text="Ваш опыт кандидата",
                            reply_markup=None)
                bot.send_message(chat_id=call.message.chat.id,
                                text="В каких проектах вы принимали участие?",
                                reply_markup=None)
            elif (progress == 29):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=30,
                                    cell_name="projects",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="""Участвовали ли вы в образовательных программах от Naumen? 
                                Если да, то расскажите об этом подробнее или поставьте прочек -""",
                                reply_markup=None)
            elif (progress == 30):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=31,
                                    cell_name="naumen_eduprogs",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Какие свои навыки вы считаете ключевыми?",
                                reply_markup=None)
            elif (progress == 31):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=32,
                                    cell_name="key_skills",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Какие у вас профессиональные интересы?",
                                reply_markup=None)
            elif (progress == 32):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=33,
                                    cell_name="prof_interests",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Какую профессиональную книгу вы прочитали последней?",
                                reply_markup=None)
            elif (progress == 33):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=34,
                                    cell_name="last_read_book",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Как вы проводите свободное время? Какие у вас увлечения?",
                                reply_markup=None)
            elif (progress == 34):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=35,
                                    cell_name="hobbies",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Что даст тебе прохождение практики в нашей компании?",
                                reply_markup=None)
            elif (progress == 35):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=36,
                                    cell_name="expectations",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Какую должность ты хочешь занять через 3-5 лет?",
                                reply_markup=None)
            elif (progress == 36):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=37,
                                    cell_name="future_rank",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Как ты узнал о компании Naumen?",
                                reply_markup=make_choose_keyboard(sources_info_naumen))
            elif (progress == 38):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=39,
                                    cell_name="source_info_naumen",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                            text="Как ты узнал о стажировке в Naumen?",
                            reply_markup=make_choose_keyboard(sources_info_naumen))
            elif (progress == 40):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=41,
                                    cell_name="source_info_internship",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="""Кто может дать вам рекомендации?
                                        (ФИО, должность, контактный телефон)""",
                                reply_markup=None)
            elif (progress == 41):
                db_funcs.update_cell(db_name='users.db',
                                    tablename='users',
                                    tg_id=message.chat.id,
                                    progress=42,
                                    cell_name="recommendations_authors",
                                    cell_value=message.text)
                bot.send_message(chat_id=message.chat.id,
                                text="Приложите ссылку на резюме на hh.ru, если оно есть или оставьте прочерк -",
                                reply_markup=None)
            elif (progress == 42):
                if (re.fullmatch(pattern="^(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,})$",
                                string=message.text) or message.text == '-'):
                    db_funcs.update_cell(db_name='users.db',
                                        tablename='users',
                                        tg_id=message.chat.id,
                                        progress=43,
                                        cell_name="summary_hhlink",
                                        cell_value=message.text)
                    bot.send_message(chat_id=message.chat.id,
                                    text="Приложите ссылку на папку с тестовым заданием в облаке",
                                    reply_markup=None)
                else:
                    bot.send_message(chat_id=message.chat.id,
                                    text="Неправильный формат, повторите ввод",
                                    reply_markup=None)
            elif (progress == 43):
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

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if (call.data in internship_cities):
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
        bot.send_message(chat_id=call.message.chat.id,
                        text="Выберите специальность",
                        reply_markup=make_choose_keyboard(internship_jobs))
    elif (call.data in internship_jobs):
        db_funcs.update_cell(db_name='users.db',
                            tablename='users',
                            tg_id=call.message.chat.id,
                            progress=2,
                            cell_name="name_internship",
                            cell_value=call.data)
        bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.id,
                            text="Выбрана специальность стажировки: %s" % call.data.lower(),
                            reply_markup=None)
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
    elif (call.data in edu_types):
        if (db_funcs.get_progress('users.db', 'users', call.message.chat.id) <= 18):
            temp_progress = 13
            temp_cellname = "`edu_type`"
        else:
            temp_progress = 19
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
                                progress=18,
                                cell_name="`edu2_exist`",
                                cell_value=1)
            bot.send_message(chat_id=call.message.chat.id,
                        text="Выберите тип полученного образования:",
                        reply_markup=make_choose_keyboard(edu_types))
        else:
            db_funcs.update_cell(db_name='users.db',
                                tablename='users',
                                tg_id=call.message.chat.id,
                                progress=24,
                                cell_name="`edu2_exist`",
                                cell_value=0)
            bot.send_message(chat_id=call.message.chat.id,
                            text="""Есть ли у вас дополнительное образование? 
                            Напишите о нем или оставьте прочерк -""",
                            reply_markup=None)
        bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.id,
                                text="Имеется второе образование: %s" % call.data,
                                reply_markup=None)
    elif (db_funcs.get_progress('users.db', 'users', call.message.chat.id) == 25):
        bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.id,
                                text="Есть ли у вас опыт работы: %s" % call.data,
                                reply_markup=None)
        if call.data.lower() == 'да':
            db_funcs.update_cell(db_name='users.db',
                                tablename='users',
                                tg_id=call.message.chat.id,
                                progress=26,
                                cell_name="jobexp_exist",
                                cell_value=1)
            bot.send_message(chat_id=call.message.chat.id,
                            text="Введите период работы (с ... до ...)",
                            reply_markup=None)
        else:
            db_funcs.update_cell(db_name='users.db',
                                tablename='users',
                                tg_id=call.message.chat.id,
                                progress=29,
                                cell_name="jobexp_exist",
                                cell_value=0)
            bot.send_message(chat_id=call.message.chat.id,
                            text="Ваш опыт кандидата",
                            reply_markup=None)
            bot.send_message(chat_id=call.message.chat.id,
                            text="В каких проектах вы принимали участие?",
                            reply_markup=None)
    elif (call.data in sources_info_naumen and
            db_funcs.get_progress('users.db', 'users', call.message.chat.id) == 37):
        bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.id,
                            text="Источник информации о компании: %s" % call.data,
                            reply_markup=None)
        if (call.data == 'другое'):
            bot.send_message(chat_id=call.message.chat.id,
                            text="Укажите источник",
                            reply_markup=None)
            db_funcs.update_progress(db_name='users.db', tablename='users',
                                    tg_id=call.message.chat.id, progress=38)
        else:
            db_funcs.update_cell(db_name='users.db',
                                tablename='users',
                                tg_id=call.message.chat.id,
                                progress=39,
                                cell_name="source_info_naumen",
                                cell_value=call.data)
            bot.send_message(chat_id=call.message.chat.id,
                            text="Как вы узнали о стажировке в Naumen?",
                            reply_markup=make_choose_keyboard(sources_info_naumen))
    elif (call.data in sources_info_naumen and
            db_funcs.get_progress('users.db', 'users', call.message.chat.id) == 39):
        bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.id,
                            text="Источник информации о стажировке: %s" % call.data,
                            reply_markup=None)
        if (call.data == 'другое'):
            bot.send_message(chat_id=call.message.chat.id,
                            text="Укажите источник",
                            reply_markup=None)
            db_funcs.update_progress(db_name='users.db', tablename='users',
                                    tg_id=call.message.chat.id, progress=40)
        else:
            db_funcs.update_cell(db_name='users.db',
                                tablename='users',
                                tg_id=call.message.chat.id,
                                progress=41,
                                cell_name="source_info_internship",
                                cell_value=call.data)
            bot.send_message(chat_id=call.message.chat.id,
                            text="Кто может дать вам рекомендации? (ФИО, должность, контактный телефон)",
                            reply_markup=None)





def create_new_form(tg_id):
    if (db_funcs.get_progress('users.db', 'users', tg_id) > 0):
        keyboard = types.InlineKeyboardMarkup()
        buttonAgree = types.InlineKeyboardButton(text='Да', callback_data='new_agree')
        buttonDisagree = types.InlineKeyboardButton(text='Отмена', callback_data='new_disagree')
        bot.send_message(chat_id=tg_id,
                        text="Ваша предыдущая анкета будет удалена, Вы уверены?",
                        reply_markup=keyboard)
    else:
        db_funcs.start_filling('users.db', 'users', tg_id)
        bot.send_message(chat_id=tg_id,
                        text='Начинаем процесс регистрации',
                        reply_markup=make_formcancel_keyboard())
        bot.send_message(chat_id=tg_id,
                        text='Выберите город прохождения стажировки',
                        reply_markup=make_choose_keyboard(internship_cities))




bot.polling(none_stop=True)
# сразу забиваем клавиатуру действий
keyboard = types.ReplyKeyboardMarkup()
buttonWorkForms = types.KeyboardButton('Работа с анкетой')
buttonShowVacancies = types.KeyboardButton('Просмотр вакансий')
keyboard.row(buttonWorkForms, buttonShowVacancies)
# это нужно, чтобы у нас не прекращалось все действо
while True:
    pass