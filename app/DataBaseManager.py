import psycopg2
import os
from dotenv import load_dotenv


class DataManager:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv("host")
        self.user = os.getenv("user")
        self.password = os.getenv("password")
        self.database = os.getenv("database")
        self.port = os.getenv("port")
        self.users = []

    def save_user_in_list(self, user):
        con = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )
        cur = con.cursor()
        cur.execute("SELECT * FROM person")
        rows = cur.fetchall()
        con.close()
        users = []
        for row in rows:
            from app.user import User

            user = User(
                row[1].strip(),
                row[2].strip(),
                row[3].strip(),
                row[4].strip(),
                row[0],
            )
            users.append(user)

        self.users = users

    def get_user_by_username(self, username):
        user = None
        self.save_user_in_list(user)
        print(self.users)
        for user in self.users:
            if user.username == username:
                return user
        return None

    def get_user_by_pass(self, password):
        for user in self.users:
            if user.password == password:
                return user
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

        id_query = "SELECT id FROM PERSON WHERE id = %s"
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

        username_query = "SELECT username FROM PERSON WHERE username = %s"
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

        email_query = "SELECT email FROM PERSON WHERE email = %s"
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

        cur.execute(
            """CREATE TABLE IF NOT EXISTS PERSON (
                ID INT ,
                NAME VARCHAR(255),
                EMAIL VARCHAR(255),
                USERNAME VARCHAR(255),
                PASSWORD_ VARCHAR(255)
            )
            """
        )

        insert_query = "INSERT INTO PERSON (id, name, email, username, password_) VALUES (%s, %s, %s, %s, %s)"
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
