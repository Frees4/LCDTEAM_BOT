import sqlite3 as sql


db_EKB = 'usersEKB.db'
db_SPB = 'usersSPB.db'
db_KRD = 'usersKRD.db'
db_TVR = 'usersTVR.db'
db_CHLB = 'usersCHLB.db'
db_users = 'users.db'

tableJava = 'internJava'
tableTester = 'internTester'
tableAnalytics = 'internAnalytics'
tableTechWriter = 'internTechwriter'
tableUsers = 'users'

def check_user_in_db(db_name, tablename, tg_id):
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

def update_cell(db_name, tablename, tg_id, progress, cell_name, cell_value):
    con = sql.connect(db_name)
    with con:
        cur = con.cursor()
        vals = (progress, cell_value, tg_id)
        query_str = "update `%s` set filling_progress=?, %s=? where tg_id=?" % (tablename, cell_name)
        cur.execute(query_str, vals)
        con.commit()
        cur.close()

def update_progress(db_name, tablename, tg_id, progress):
    con = sql.connect(db_name)
    with con:
        cur = con.cursor()
        vals = (progress, tg_id)
        cur.execute("update `%s` set filling_progress=? where tg_id=?" % tablename, vals)
        con.commit()
        cur.close()

def start_filling(db_name, tablename, tg_id):
    con = sql.connect(db_name)
    with con:
        cur = con.cursor()
        cur.execute("update `%s` set filling_form=1, filling_progress=0 where tg_id=?" % tablename, (tg_id,))
        con.commit()
        cur.close()

def end_filling(db_name, tablename, tg_id):
    con = sql.connect(db_name)
    with con:
        cur = con.cursor()
        cur.execute("update `%s` set filling_form=0 where tg_id=?" % tablename, (tg_id,))
        con.commit()
        cur.close()

def get_progress(db_name, tablename, tg_id):
    con = sql.connect(db_name)
    with con:
        cur = con.cursor()
        cur.execute("select filling_progress from `%s` where tg_id=?" % tablename, (tg_id,))
        result = cur.fetchone()
        con.commit()
        cur.close()
        return result[0]

def check_filling(db_name, tablename, tg_id):
    con = sql.connect(db_name)
    with con:
        cur = con.cursor()
        cur.execute("select filling_form from `%s` where tg_id=?" % tablename, (tg_id,))
        result = cur.fetchone()
        con.commit()
        cur.close()
        return result[0]

def add_user_to_db(db_name, tablename, tg_id):
    con = sql.connect(db_name)
    with con:
        cur = con.cursor()
        vals = (tg_id, 1, 0)
        cur.execute("INSERT INTO `%s` (tg_id, filling_form, filling_progress) VALUES (?, ?, ?)" % tablename,
                    vals)
        con.commit()
        cur.close()

def get_userdata(db_name, tablename, tg_id):
    con = sql.connect(db_name)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM `%s` where tg_id=?" % tablename, (tg_id,))
        results = cur.fetchone()
        con.commit()
        cur.close()
        

def delete_user_from_db(db_name, tablename, tg_id):
    con = sql.connect(db_name)
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM `%s` where tg_id = ?" % tablename, (tg_id,))
        con.commit()
        cur.close()