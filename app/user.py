from random import randrange
from .DataBaseManager import DataManager


class User:
    def __init__(self, name, email, username, password, user_id):
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.email_ver = False
        self.password_ver = False
        self.user_ID = user_id
        self.data_manager = DataManager()

    def print_user_id(self):
        return self.user_ID

    def change_password(self, new_password):
        self.password = new_password

    def change_email(self, new_email):
        self.email = new_email

    def get_email(self):
        return self.email

    def __str__(self):
        return f"{self.username} - {self.user_ID}"

    def save_data(self):
        self.data_manager.save_user(self)
