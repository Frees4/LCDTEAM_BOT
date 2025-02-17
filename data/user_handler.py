import sqlite3 as sql

class UserHandler:
    def __init__(self):
        self.db_vacancies = 'data/vacancies.db'
        self.db_users = 'data/users.db'
    def check_user_in_db(self, db_name, tablename, tg_id):
        con = sql.connect(db_name)
        with con:
            cur = con.cursor()
            cur.execute("SELECT `tg_id` from `%s`" % tablename)
            rows = cur.fetchall()
            con.commit()
            cur.close()
            for row in rows:
                if (row[0] == tg_id):
                    return True
            return False

    def add_user_to_subscribers(self, tg_id):
        con = sql.connect(self.db_users)
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO `subscribers` (tg_id) VALUES (?)", (tg_id,))
            con.commit()
            cur.close()

    def get_users_notfilled(self):
        con = sql.connect(self.db_users)
        with con:
            cur = con.cursor()
            cur.execute("SELECT `tg_id` from `users` where `filling_progress` < 100 and `filling_form` == 1")
            rows = cur.fetchall()
            con.commit()
            cur.close()
            results = []
            for row in rows:
                results.append(row[0])
            return results

    def clear_table_vacancies(self, tablename):
        con = sql.connect(self.db_vacancies)
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM `%s`" % tablename)
            con.commit()
            cur.close()

    def change_vacancies(self, tablename, values):
        con = sql.connect(self.db_vacancies)
        with con:
            cur = con.cursor()
            for value in values:
                cur.execute("INSERT INTO `%s` (name_internship) VALUES (?)" % tablename, (value,))
            con.commit()
            cur.close()

    def get_parameters(self, db_name, tablename, parameter):
        con = sql.connect(db_name)
        with con:
            cur = con.cursor()
            cur.execute("SELECT %s FROM `%s`" % (parameter, tablename))
            rows = cur.fetchall()
            con.commit()
            cur.close()
            results = []
            for row in rows:
                results.append(row[0])
            return results


    def get_new_id(self, db_name, tablename):
        con = sql.connect(db_name)
        with con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(id) FROM %s" % tablename)
            length = cur.fetchone()[0]
            con.commit()
            cur.close()
            return length+1

    def add_forminfo_table(self, db_name, tablename, td_id, vals):
        con = sql.connect(db_name)
        with con:
            cur = con.cursor()
            query_str = "INSERT INTO `%s` " % tablename
            query_str += "(id, tg_id, surname_intern, name_intern, patronymics_intern, "
            query_str += "date_of_birth, city_living, email, telnumber, date_of_start, "
            query_str += "time_spend, work_after_internship, edu_type, edu_name, "
            query_str += "edu_year_start, edu_year_end, edu_faculty, edu_score, "
            query_str += "edu2_type, edu2_name, edu2_year_start, edu2_year_end, "
            query_str += "edu2_faculty, edu2_score, additive_edu, jobexp_exist, time1, place1, "
            query_str += "rank1, duty1, time2, place2, rank2, duty2, "
            query_str += "time3, place3, rank3, duty3, "
            query_str += "time4, place4, rank4, duty4, "
            query_str += "projects, naumen_eduprogs, key_skills, prof_interests, "
            query_str += "last_read_book, hobbies, expectations, future_rank, source_info_naumen, "
            query_str += "source_info_internship, recommendations_authors, summary_hhlink, task_link)"
            query_str += "VALUES ("
            for i in range(54):
                query_str += "?, "
            query_str += "?)"
            cur.execute(query_str, vals)
            con.commit()
            cur.close()

    def update_cell(self, db_name, tablename, tg_id, progress, cell_name, cell_value):
        con = sql.connect(db_name)
        with con:
            cur = con.cursor()
            vals = (progress, cell_value, tg_id)
            query_str = "update `%s` set filling_progress=?, %s=? where tg_id=?" % (tablename, cell_name)
            cur.execute(query_str, vals)
            con.commit()
            cur.close()

    def update_progress(self, db_name, tablename, tg_id, progress):
        con = sql.connect(db_name)
        with con:
            cur = con.cursor()
            vals = (progress, tg_id)
            cur.execute("update `%s` set filling_progress=? where tg_id=?" % tablename, vals)
            con.commit()
            cur.close()

    def get_progress(self, db_name, tablename, tg_id):
        con = sql.connect(db_name)
        with con:
            cur = con.cursor()
            cur.execute("select filling_progress from `%s` where tg_id=?" % tablename, (tg_id,))
            result = cur.fetchone()
            con.commit()
            cur.close()
            return result[0]