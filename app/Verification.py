from getpass import getpass
from .user import User
from .DataBaseManager import DataManager
from random import randrange
import re


class Authorization:
    def __init__(self):
        self.data_manager = DataManager()

    def authenticate_user(self):
        username = input("Username: ")
        password = getpass("Password: ")
        user_data = self.data_manager.get_user_by_username(username)
        user_log = self.data_manager.check_user_log(username)
        if user_log:
            if user_data is not None:
                if password == user_data.password:
                    name = user_data.name
                    email = user_data.email
                    username = user_data.username
                    password = user_data.password
                    user_id = user_data.user_ID
                    user = User(name, email, username, password, user_id)
                    print("Authentication successful!")
                    return user
                else:
                    print("Invalid password!")
            else:
                print("User not found!")
        else:
            print("User is already logged in!")

        return None

    def register_user(self):
        self.data_manager.create_users_table()
        name = input("Name: ")
        email = input("Email: ")
        username = input("Username: ")
        password = getpass("Password: ")
        password_again = getpass("Password (again): ")
        password = self.verify_password(password, password_again)
        email = self.verify_email(email)
        username = self.verify_username(username)
        email = self.valid_email(email)
        while True:
            user_id = randrange(100, 10000)
            if not self.data_manager.is_id_taken(user_id):
                break

        user = User(name, email, username, password, user_id)
        user.save_data()
        print("User created successfully!")
        print(user)
        return user

    def authorize_user(self):
        while True:
            choice = input("1. Login\n2. Register\n3. Exit\nEnter your choice: ")

            if choice == "1":
                user = self.authenticate_user()
                if user:
                    return user
            elif choice == "2":
                user = self.register_user()
                if user:
                    return user
            elif choice == "3":
                return None
            else:
                print("Invalid choice. Please try again.")

    def verify_password(self, password, again_password):
        numbers = False
        special_symbol = False
        len_11 = False
        upper_case = False
        count_up = 0
        if password != again_password and len(password) < 11:
            print("Passwords do not match!")
        else:
            len_11 = True
            for element in password:
                if element.isdigit():
                    numbers = True
                if not element.isalnum():
                    special_symbol = True
                if element.isupper():
                    count_up += 1
                    if count_up >= 2:
                        upper_case = True
            return password

        if not len_11:
            print("Password length should be at least 11 characters.")
        elif not numbers:
            print("Password should contain at least one digit.")
        elif not special_symbol:
            print("Password should contain at least one special symbol.")
        elif not upper_case:
            print("Password should contain at least two uppercase letters.")
        else:
            print("Password is valid!")

    def verify_username(self, username):
        data_manager = self.data_manager
        while data_manager.is_username_taken(username):
            print("Username is already taken. Please choose a different username.")
            username = input("Enter a valid username: ")
        return username

    def valid_email(self, email):
        data_manager = self.data_manager
        while data_manager.is_email_taken(email):
            print("Email is already taken. Please choose a different email.")
            email = input("Enter a valid email: ")
        return email

    def verify_email(self, email):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        if re.fullmatch(regex, email):
            print("Valid Email")
            return email
        else:
            print("Invalid Email")
