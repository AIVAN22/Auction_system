from random import randrange
from .Verification import verify_password, verify_email, verify_username, valid_email
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
        return f"User: {self.username} with ID: {self.user_ID}"

    def verification_password(self):
        self.password = verify_password(self.password, self.again_password)
        if self.password:
            self.password_ver = True

    def verification_email(self):
        self.email = verify_email(self.email)
        if self.email:
            self.email_ver = True

    def verification_username(self):
        self.username = verify_username(self.username)

    def is_email_valid(self):
        self.email = valid_email(self.email)

    def save_data(self):
        self.data_manager.save_user(self)
