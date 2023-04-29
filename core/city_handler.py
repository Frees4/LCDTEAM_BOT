import sqlite3 as sql

class CityHandler:
    def __init__(self):
        self.db_cities = 'cities.db'

    def check_city_in_db(self, city_name):
        con = sql.connect(self.db_cities)
        with con:
            cur = con.cursor()
            cur.execute("SELECT `name` from `cities`")
            rows = cur.fetchall()
            con.commit()
            cur.close()
            for row in rows:
                if (row[0].lower() == city_name.lower()):
                    return True
            return False

    def add_city(self, city_name):
        con = sql.connect(self.db_cities)
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO `cities` (name) VALUES (?)", (city_name,))
            con.commit()
            cur.close()

    def get_all_cities(self):
        con = sql.connect(self.db_cities)
        with con:
            cur = con.cursor()
            cur.execute("SELECT `name` from `cities`")
            rows = cur.fetchall()
            con.commit()
            cur.close()
            results = []
            for row in rows:
                results.append(row[0])
            return results
