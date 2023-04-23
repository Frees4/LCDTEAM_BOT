import sqlite3 as sql

class UserCRUDHandler:
    def __init__(self):
        self.db_vacancies = 'vacancies.db'
        self.db_users = 'users.db'
    # Create
    def add_user_to_db(self, db_name, tablename, tg_id):
        con = sql.connect(db_name)
        with con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(id) FROM %s" % tablename)
            length = cur.fetchone()[0]
            vals = (length+1, tg_id, 1, 0)
            cur.execute("INSERT INTO `%s` (id, tg_id, filling_form, filling_progress) VALUES (?, ?, ?, ?)" % tablename,
                        vals)
            con.commit()
            cur.close()

    # Read
    def get_userdata(self, db_name, tablename, tg_id):
        con = sql.connect(db_name)
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM `%s` where tg_id=?" % tablename, (tg_id,))
            results = cur.fetchone()
            con.commit()
            cur.close()
        return results
    
    # Update
    def start_filling(self, db_name, tablename, tg_id):
        con = sql.connect(db_name)
        with con:
            cur = con.cursor()
            cur.execute("update `%s` set filling_form=1, filling_progress=0 where tg_id=?" % tablename, (tg_id,))
            con.commit()
            cur.close()

    def end_filling(self, db_name, tablename, tg_id):
        con = sql.connect(db_name)
        with con:
            cur = con.cursor()
            cur.execute("update `%s` set filling_form=0 where tg_id=?" % tablename, (tg_id,))
            con.commit()
            cur.close()
            
    def check_filling(self, db_name, tablename, tg_id):
        con = sql.connect(db_name)
        with con:
            cur = con.cursor()
            cur.execute("select filling_form from `%s` where tg_id=?" % tablename, (tg_id,))
            result = cur.fetchone()
            con.commit()
            cur.close()
            return result[0]

    # Delete
    def delete_user_from_db(self, db_name, tablename, tg_id):
        con = sql.connect(db_name)
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM `%s` where tg_id = ?" % tablename, (tg_id,))
            con.commit()
            cur.close()