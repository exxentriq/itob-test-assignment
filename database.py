import os
import sqlite3
from datetime import date

from dotenv import load_dotenv


load_dotenv() # Take environment variables from .env

DATABASE = os.getenv("SQLITE3_DATABASE")


class Database:
    def __init__(self):
        """Creates database structure if it does not exist"""

        print(DATABASE)
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS kettle_records (
                id integer PRIMARY KEY AUTOINCREMENT,
                kettle_state varchar(3),
                water_level_liters float,
                water_temperature_celsius float,
                message text,
                time timestamp
        )
        """)

        con.commit()
        con.close()

    def insert_data(self, data: tuple):
        """Insert data into database"""

        con = sqlite3.connect(DATABASE)
        cur = con.cursor()

        cur.execute("""INSERT INTO kettle_records(kettle_state, water_level_liters, water_temperature_celsius, message, time)
                            VALUES (?, ?, ?, ?, ?)""", data)

        con.commit()
        con.close()

    def read_all_records(self):
        """Reads all database records"""

        con = sqlite3.connect(DATABASE)
        cur = con.cursor()

        records_list = []

        for row in cur.execute(f"""
            SELECT id, kettle_state, water_level_liters, water_temperature_celsius, message, time
            FROM kettle_records
        """):
            records_list.append({
                "id": row[0],
                "kettle_state": row[1],
                "water_level_liters": row[2],
                "water_temperature_celsius": row[3],
                "message": row[4],
                "time": row[5]
            })

        con.close()
        
        return records_list

    def read_last_record(self):
        """Reads last database record"""

        con = sqlite3.connect(DATABASE)
        cur = con.cursor()

        last_row = cur.execute(f"""
            SELECT id, kettle_state, water_level_liters, water_temperature_celsius, message, time
            FROM kettle_records ORDER BY id DESC LIMIT 1
        """).fetchone()
        
        last_record = {
            "id": last_row[0],
            "kettle_state": last_row[1],
            "water_level_liters": last_row[2],
            "water_temperature_celsius": last_row[3],
            "message": last_row[4],
            "time": last_row[5]
        }

        con.close()
        
        return last_record