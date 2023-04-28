# from city_handler import CityHandler
from data.user_handler import UserHandler
from data.user_crud_handler import UserCRUDHandler
from spreadsheet.google_spreadsheet import Spreadsheet
from keyboard_handler import KeyboardHandler
from bot_handler import BotHandler


class Facade:
    def __init__(self):
#        self.city_handler = CityHandler()
#        self.city_crud_handler = CityCRUDHandler()
        self.user_handler = UserHandler()
        self.user_crud_handler = UserCRUDHandler()
        self.keyboard_handler = KeyboardHandler()
        self.spreadsheet = Spreadsheet()
        self.bot_handler = BotHandler()

    # Методы CityHandler

    # Методы UserHandler
    def check_user_in_db(self, db_name, tablename, tg_id):
        return self.user_handler.check_user_in_db(db_name, tablename, tg_id)

    def add_user_to_subscribers(self, tg_id):
        return self.user_handler.add_user_to_subscribers(tg_id)

    def get_users_notfilled(self):
        return self.user_handler.get_users_notfilled()

    def clear_table_vacancies(self, tablename):
        return self.user_handler.clear_table_vacancies(tablename)

    def change_vacancies(self, tablename, values):
        return self.user_handler.change_vacancies(tablename, values)

    def get_parameters(self, db_name, tablename, parameter):
        return self.user_handler.get_parameters(db_name, tablename, parameter)

    def get_new_id(self, db_name, tablename):
        return self.user_handler.get_new_id(db_name, tablename)
    
    def add_forminfo_table(self, db_name, tablename, td_id, vals):
        return self.user_handler.add_forminfo_table(db_name, tablename, td_id, vals)

    def update_cell(self, db_name, tablename, tg_id, progress, cell_name, cell_value):
        return self.user_handler.update_cell(db_name, tablename, tg_id, progress, cell_name, cell_value)
    
    def update_progress(self, db_name, tablename, tg_id, progress):
        return self.user_handler.update_progress(db_name, tablename, tg_id, progress)

    def get_progress(self, db_name, tablename, tg_id):
        return self.user_handler.get_progress(db_name, tablename, tg_id)

    # Методы Spreadsheet
    def add_new_trainee(self, table_id, list_name, values, id_bd):
        return self.spreadsheet.add_new_trainee(table_id, list_name, values, id_bd)
    
    def get_forms_list(self, tg_id):
        return self.spreadsheet.get_forms_list(tg_id)

    # Методы KeyboardHandler
    def make_actions_endfill_keyboard(self):
        return self.keyboard_handler.make_actions_endfill_keyboard()
    
    def make_choose_keyboard(self, items_list):
        return self.keyboard_handler.make_choose_keyboard(items_list)
    
    def make_choose_timespend_keyboard(self):
        return self.keyboard_handler.make_choose_timespend_keyboard()
    
    def make_choose_job_keyboard(self):
        return self.keyboard_handler.make_choose_job_keyboard()
    
    def make_choose_city_keyboard(self):
        return self.keyboard_handler.make_choose_city_keyboard()
    
    def make_form_actions_keyboard(self, tg_id):
        return self.keyboard_handler.mmake_form_actions_keyboard(tg_id)
    
    def make_welcome_actions_keyboard(self):
        return self.keyboard_handler.make_welcome_actions_keyboard()
    
    def make_formcancel_keyboard(self):
        return self.keyboard_handler.make_formcancel_keyboard()


    # Методы CityCRUDHandler

    # Методы UserCrudHandler
    def add_user_to_db(self, db_name, tablename, tg_id):
        return self.user_crud_handler.add_user_to_db(db_name, tablename, tg_id)
    
    def get_userdata(self, db_name, tablename, tg_id):
        return self.user_crud_handler.get_userdata(db_name, tablename, tg_id)
    
    def start_filling(self, db_name, tablename, tg_id):
        return self.user_crud_handler.start_filling(db_name, tablename, tg_id)
    
    def check_filling(self, db_name, tablename, tg_id):
        return self.user_crud_handler.check_filling(db_name, tablename, tg_id)

    def end_filling(self, db_name, tablename, tg_id):
        return self.user_crud_handler.end_filling(db_name, tablename, tg_id)
    
    def delete_user_from_db(self, db_name, tablename, tg_id):
        return self.user_crud_handler.delete_user_from_db(db_name, tablename, tg_id)
    
    # Методы BotHandler
    def get_forms(self, bot, tg_id):
        return self.bot_handler.get_forms(bot, tg_id)
    
    def get_vacancies_list(self, tag):
        return self.bot_handler.get_vacancies_list(tag)
    
    def show_vacancies(self, bot, tg_id, tag):
        return self.bot_handler.show_vacancies(bot, tg_id, tag)
    
    def show_vacancy_cities(self, bot, tg_id):
        return self.bot_handler.show_vacancy_cities(bot, tg_id)
    
    def show_form(self, bot, tg_id):
        return self.bot_handler.show_form(bot, tg_id)
    
    def send_form(self, bot, tg_id):
        return self.bot_handler.send_form(bot, tg_id)
