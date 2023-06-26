import psycopg2
import os
from dotenv import load_dotenv
import datetime


class DataManager:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv("host")
        self.user = os.getenv("user")
        self.password = os.getenv("password")
        self.database = os.getenv("database")
        self.port = os.getenv("port")

    def create_users_table(self):
        con = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS Users (
                ID INT ,
                NAME VARCHAR(255),
                EMAIL VARCHAR(255),
                USERNAME VARCHAR(255),
                PASSWORD_ VARCHAR(255)
            )
            """
        )

        con.commit()
        con.close()

    def get_user_by_username(self, username):
        con = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )
        cur = con.cursor()

        username_query = "SELECT * FROM users WHERE username = %s"
        cur.execute(username_query, (username,))
        existing_username = cur.fetchone()
        if existing_username:
            from app.user import User

            user = User(
                existing_username[1].strip(),
                existing_username[2].strip(),
                existing_username[3].strip(),
                existing_username[4].strip(),
                existing_username[0],
            )
            return user
        else:
            return None

    def is_id_taken(self, user_id):
        con = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )
        cur = con.cursor()

        id_query = "SELECT id FROM users WHERE id = %s"
        cur.execute(id_query, (user_id,))
        existing_id = cur.fetchone()

        con.close()

        return existing_id is not None

    def is_username_taken(self, username):
        con = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )
        cur = con.cursor()

        username_query = "SELECT username FROM users WHERE username = %s"
        cur.execute(username_query, (username,))
        existing_username = cur.fetchone()

        con.close()

        return existing_username is not None

    def is_email_taken(self, email):
        con = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )
        cur = con.cursor()

        email_query = "SELECT email FROM users WHERE email = %s"
        cur.execute(email_query, (email,))
        existing_email = cur.fetchone()

        con.close()

        return existing_email is not None

    def save_user(self, user):
        con = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )
        cur = con.cursor()

        insert_query = "INSERT INTO Users (id, name, email, username, password_) VALUES (%s, %s, %s, %s, %s)"
        values = (
            user.user_ID,
            user.name,
            user.email,
            user.username,
            user.password,
        )
        cur.execute(insert_query, values)
        con.commit()
        con.close()

    def save_logs(self, username, status):
        con = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS users_logs (
                        USERNAME VARCHAR(255),
                        time TIMESTAMP,
                        status varchar(255)
                    )
                    """
        )
        insert_query = (
            "INSERT INTO users_logs (username, time ,status) VALUES (%s, %s,%s)"
        )
        values = (
            username,
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status,
        )
        cur.execute(insert_query, values)
        con.commit()
        con.close()

    def check_user_log(self, username):
        con = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )

        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS users_logs (
                USERNAME VARCHAR(255),
                time TIMESTAMP,
                status varchar(255)
            )
            """
        )
        last_log_query = "SELECT status FROM users_logs WHERE username = %s  ORDER BY time DESC LIMIT 1"
        cur.execute(last_log_query, (username,))
        last_log = cur.fetchone()
        con.close()

        is_last_log_out = False
        if last_log is None or last_log[0] == "Log out":
            is_last_log_out = True
        return is_last_log_out


class RoomManager(DataManager):
    def __init__(self):
        super().__init__()

    def create_room_table(self):
        con = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS ROOMs (
                ID int,
                NAME VARCHAR(255),
                Item_name VARCHAR(255),
                price VARCHAR(255),
                time VARCHAR(255),
                STATUS VARCHAR(255)
            )"""
        )
        con.commit()
        con.close()

    def is_room_exists(self, name):
        con = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )
        cur = con.cursor()

        select_query = "SELECT * FROM ROOMs WHERE NAME = %s"
        cur.execute(select_query, (name,))
        existing_room = cur.fetchone()

        return existing_room is not None

    def get_rooms(self):
        con = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )
        cur = con.cursor()

        select_query = "SELECT * FROM ROOMs"
        cur.execute(select_query)
        existing_rooms = cur.fetchall()

        con.close()

        return existing_rooms

    def get_room_by_id(self, room_id):
        con = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )
        cur = con.cursor()

        select_query = "SELECT * FROM ROOMs where id = %s"
        cur.execute(select_query, (room_id,))
        existing_room = cur.fetchall()[0]

        con.close()

        return existing_room

    def create_room(self, name, status):
        con = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )
        cur = con.cursor()
        insert_query = "INSERT INTO ROOMs (name, status) VALUES (%s, %s)"
        values = (name, status)
        cur.execute(insert_query, values)
        con.commit()
        con.close()

    def add_room(self, name, item, price, time, status):
        con = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )
        cur = con.cursor()
        insert_query = "INSERT INTO ROOMs (name, item,price,time , status) VALUES (%s, %s, %s, %s, %s)"
        values = (name, item, price, time, status)
        cur.execute(insert_query, values)
        con.commit()
        con.close()


class ItemManager(DataManager):
    def __init__(self):
        super().__init__()

    def create_items_table(self):
        con = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS items (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                price NUMERIC(10, 2)
            )"""
        )
        con.commit()
        con.close()

    def add_item_to_database(self, name, price):
        con = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )
        cur = con.cursor()

        insert_query = "INSERT INTO items (name, price) VALUES (%s, %s)"
        values = (name, price)
        cur.execute(insert_query, values)
        con.commit()
        con.close()
