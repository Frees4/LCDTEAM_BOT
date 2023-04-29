import sqlite3 as sql

class CityCRUDHandler:
    # Create
    def add_city_to_db(self, db_name, tablename, name):
        con = sql.connect(db_name)
        with con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(id) FROM %s" % tablename)
            length = cur.fetchone()[0]
            vals = (length+1, name)
            cur.execute("INSERT INTO `%s` (id, name) VALUES (?, ?)" % tablename,
                        vals)
            con.commit()
            cur.close()

    # Read
    def get_citydata(self, db_name, tablename, city_id):
        con = sql.connect(db_name)
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM `%s` where id=?" % tablename, (city_id,))
            results = cur.fetchone()
            con.commit()
            cur.close()
        return results
    
    def get_all_cities(self, db_name, tablename):
        con = sql.connect(db_name)
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM `%s`" % tablename)
            results = cur.fetchall()
            con.commit()
            cur.close()
        return results

    # Update
    def update_city(self, db_name, tablename, city_id, new_name):
        con = sql.connect(db_name)
        with con:
            cur = con.cursor()
            cur.execute("update `%s` set name=? where id=?" % tablename, (new_name, city_id))
            con.commit()
            cur.close()

    # Delete
    def delete_city_from_db(self, db_name, tablename, city_id):
        con = sql.connect(db_name)
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM `%s` where id = ?" % tablename, (city_id,))
            con.commit()
            cur.close() 
