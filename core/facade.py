# from city_handler import CityHandler
from data.user_handler import UserHandler
from data.user_crud_handler import UserCRUDHandler
from spreadsheet import google_funcs


class Facade:
    def __init__(self):
#        self.city_handler = CityHandler()
#        self.city_crud_handler = CityCRUDHandler()
        self.user_handler = UserHandler()
        self.user_crud_handler = UserCRUDHandler()
#        self.spreadsheet = Spreadsheet()

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
